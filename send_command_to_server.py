#!/usr/bin/env python3
#pylint: disable=no-init
#pylint: disable=no-self-use
#pylint: disable=no-member
#pylint: disable=abstract-class-little-used
#pylint: disable=unused-variable

''' This program sends a command to the server
    and transforms its output in a readable view.
'''

import re
import paramiko
import socket

class DataGetter:
    ''' Abstract class for any data downloader. '''

    def get_output(self):
        ''' Dowload all information from given ip_address address.
            Return string value, containing downloaded data.
        '''
        raise NotImplementedError

    def parse_output(self):
        ''' Parse given data. '''
        raise NotImplementedError

class SshDataGetter(DataGetter):
    ''' Implementationt of DataGetter. '''

    def __init__(self):
        self.command = ''
        self.username = ''
        self.ip_address = ''
        self.password = ''
        self.output_data = ''

    def split_to_values(self, given_string):
        ''' Method splits a string to list of values. '''
        given_string = given_string.strip()
        comand_begin = given_string.find("'")
        comand_end = given_string.find("'", comand_begin + 1)
        string = given_string[:comand_begin - 1] + given_string[comand_end + 1:]
        words = string.split(' ')
        for word in words:
            if word == "":
                words.remove(word)
        words.append(given_string[comand_begin + 1:comand_end])
        return words

    def get_values(self, string):
        ''' Method assigns data to specified fields. '''
        list_of_values = self.split_to_values(string)
        self.username = list_of_values[2]
        self.ip_address = list_of_values[3]
        self.password = list_of_values[4]
        self.command = list_of_values[5]

    def get_output(self):
        '''
            Method connects to server, execute the command and returns the
            output.
        '''
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.ip_address, username=self.username, password=self.password, port=22)
        shell = client.invoke_shell()
        shell.settimeout(1)
        shell.send(self.command + '\n')
        out = ''
      # import pdb; pdb.set_trace()
        while True:
            try:
                my_out = shell.recv(1000)
                my_out = my_out.decode('UTF-8')
          #      print ('my_out: ', my_out)
                if my_out != out:
                    out = my_out
                    self.output_data += my_out
           #         shell.send('\n')
            #        print(' \\n sent')
            except socket.timeout:
                break
    #    print(self.output_data)
        client.close()
        return self.output_data

    def parse_output(self):
        '''
            Method parses output and returns required data in format 'x.y'.
            If it was not found, method returns None.
        '''
        required_out = re.search(r'[\d]+\.[\d]+', self.output_data)
        if required_out:
            return required_out.group()
        else:
            return None

    def parse_all_volumes(self):
        '''
            Method parses output and returns a list of tuples.
            A tuple contains a value and unit of VOLUME found.
            If a VOLUME was not found, method returns None.
        '''
        volumes = re.findall(r'([\d]+\.[\d]+)([KMGTPE]B)', self.output_data)
        if volumes:
            return volumes
        else:
            return None

    def get_current_volume(self, vdisk_index):
        ''' Method gets volume of vdisk by given index of disk. '''
        self.command = "show volumes"
        out = self.get_output();
        return self.parse_current_volume(vdisk_index)

    def parse_current_volume(self, vdisk_index):
        ''' Method parses volume of vdisk by given index of disk. '''
        volumes = self.parse_all_volumes()
        volumes_gb = self.convert_volume_to_gb(volumes)
        return str(volumes_gb[vdisk_index]) + 'GB'

    def get_number_of_volumes(self):
        ''' Method returns number of vdisks. '''
        self.command = "show volumes"
        out = self.get_output();
        volumes = self.parse_all_volumes()
        return len(volumes)

    def convert_volume_to_gb(self, volumes):
        ''' Converts given volume in GB '''
        volumes_gb = []
        for value in volumes:
            unit = value[1]
            count = value[0]
            if unit == 'MB':
                volumes_gb.append(float(count) / pow(1000, 1))
            elif unit == 'KB':
                volumes_gb.append(float(count) / pow(1000, 2))
            elif unit == 'TB':
                volumes_gb.append(float(count) * pow(1000, 1))
            elif unit == 'PB':
                volumes_gb.append(float(count) * pow(1000, 2))
            elif unit == 'EB':
                volumes_gb.append(float(count) * pow(1000, 3))
            else:
                volumes_gb.append(float(count))
        return volumes_gb

    def get_total_volume(self):
        ''' Method gets total volume from server '''
        self.command = "show volumes"
        out = self.get_output();
        return self.parse_total_volume()

    def parse_total_volume(self):
        '''
            Method parses output and returns a total VOLUME in GB.
            If a VOLUME was not found, method returns None.
        '''
        volumes = self.parse_all_volumes()
        if volumes:
            total_volume = 0
            for volume in self.convert_volume_to_gb(volumes):
                total_volume += volume
            return str(total_volume) + 'GB'
        else:
            return None

    def get_temperature(self):
        ''' Method gets temperatures of each sensor from server '''
        self.command = "show sensor-status"
        out = self.get_output()
        return self.parse_temperature()

    def parse_temperature(self):
        '''
            Method parses output and returns a list of all temperatures,
            which was found. If a temperature was not found, it returns None.
        '''
        data = re.findall(r'(\S+ \S+)[ ]+([\d]+[\s]+C)', self.output_data)
        data = dict(data)
        if data:
            return data
        else:
            return None

    def get_disks_helth(self):
        ''' Method gets Helth of all disks. '''
        self.command = 'show disks'
        out = self.get_output()
        return self.parse_disk_helth()

    def parse_disks_helth(self):
        '''
            Method parses out and return a dictionary with Location as a key
            and Health as a value
        '''
        helth = re.findall(r'^(\d+\.\d)( +\S+){7} +(\S+)', self.output_data)
        helth_dict = {}
        for elem in helth:
            helth_dict.update({elem[0] : elem[2]})
        return helth_dict

if __name__ == '__main__':
    SSH_GETTER = SshDataGetter()
    SSH_GETTER.ip_address = "127.0.0.1"
    SSH_GETTER.password = "Lubitleto"
    SSH_GETTER.username = "maria"
    TOTAL_VOLUME = SSH_GETTER.get_total_volume()
    print ('Total volume: \n', TOTAL_VOLUME)
    NUMBER_OF_VDISKS = SSH_GETTER.get_number_of_volumes()
    print ('Number of vdisks: ', NUMBER_OF_VDISKS)
    CURRENT_VOLUME = SSH_GETTER.get_current_volume(0)
    print ('Volume of 0 disk: ', CURRENT_VOLUME)
    RESULT_TEMP = SSH_GETTER.get_temperature()
    print("Temperatures:")
    for TEMP in RESULT_TEMP:
        print(TEMP)
