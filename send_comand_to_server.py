#!/usr/bin/env python3
''' This program sends a comand to the server
    and transform its output in a readable view.
'''

import os
import paramiko
import os

class DataGetter:
    ''' Abstract class for any data downloader. '''

    def get_data(self, string):
        ''' Dowload all informayion from given ip address.
            Return string value, containing downloaded data.
        '''
        pass

    def parse_data(self, data):
        ''' Parse given data. '''
        pass

class SshDataGetter(DataGetter):
    ''' Implementationt of DataGetter. '''

    def __init__(self):
        self.comand = ''
        self.username = ''
        self.ip = ''
        self.password = ''
        self.data = ''

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
        self.ip = list_of_values[3]
        self.password = list_of_values[4]
        self.comand = list_of_values[5]

    def get_my_data(self):
        my_file = open('/home/maria/prog/sfd/scts/my_data', 'r')
        data = my_file.readlines()
        self.ip = data[0]
        self.username = data[1]
        self.password = data[2]
        my_file.close()


    def get_data(self):
        ''' Method connects to server and sends the comand. '''
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print ('before connection')
        ssh.connect(self.ip, username=self.username, password=self.password)
        print ('after connection')
        stdin, stdout, stderr = ssh.exec_command(self.comand)
        self.data = stdout.read()
        ssh.close()
        return self.data
