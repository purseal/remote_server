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
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.ip_address, username=self.username,
                       password=self.password, port=22)
        stdin, stdout, stderr = client.exec_command(self.command)
        output = stdout.read() + stderr.read()
        client.close()
        if output is not None:
            output = output[:-1]
            output = output.decode('UTF-8')
            self.output_data = output
        else:
            self.output_data = None
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

    def get_total_volume(self):
        '''
            Method parses output and returns a total VOLUME in GB.
            If a VOLUME was not found, method returns None.
        '''
    #    self.command = "show volumes"
    #    out = self.get_output();
        volumes = self.parse_all_volumes()
        if volumes:
            total_volume = 0
            for value in volumes:
                unit = value[1]
                count = value[0]
                if unit == 'MB':
                    total_volume += float(count) / pow(1000, 1)
                elif unit == 'KB':
                    total_volume += float(count) / pow(1000, 2)
                elif unit == 'TB':
                    total_volume += float(count) * pow(1000, 1)
                elif unit == 'PB':
                    total_volume += float(count) * pow(1000, 2)
                elif unit == 'EB':
                    total_volume += float(count) * pow(1000, 3)
                else:
                    total_volume += float(count)
            return str(total_volume) + 'GB'
        else:
            return None

    def parse_temperature(self):
        '''
            Method parses output and returns a list of all temperatures,
            which was found. If a temperature was not found, it returns None.
        '''
     #   self.command = "show sensor-status"
     #   out = self.get_output()
        temp = re.findall(r'[\d]+[\s]+C', self.output_data)
        if temp:
            return temp
        else:
            return None

if __name__ == '__main__':
    SSH_GETTER = SshDataGetter()
    SSH_GETTER.ip_address = "127.0.0.1"
    SSH_GETTER.password = "Lubitleto"
    SSH_GETTER.username = "maria"
    RESULT_VOLUMES = SSH_GETTER.get_total_volume()
    RESULT_TEMP = SSH_GETTER.parse_temperature()
    print("List of volumes:")
    for VOLUME in RESULT_VOLUMES:
        print(VOLUME)
    print("Temperatures:")
    for TEMP in RESULT_TEMP:
        print(TEMP)
