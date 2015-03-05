#!/usr/bin/env python3
''' This program sends a command to the server
    and transform its output in a readable view.
'''

from subprocess import Popen, PIPE

class DataGetter:
    ''' Abstract class for any data downloader. '''

    def get_data(self):
        ''' Dowload all information from given ip_address address.
            Return string value, containing downloaded data.
        '''
        raise NotImplementedError

    def parse_data(self, data):
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

    def get_data(self):
        ''' Method connects to server and sends the command. '''
        terminal_command = 'sshpass -p {} ssh -o '.format(self.password + '\n')
        terminal_command += 'StrictHostKeyChecking=no {}'.format(
            self.ip_address + '\n'
            )
        terminal_command += self.command
        terminal_command_list = terminal_command.split()
        proc = Popen(terminal_command_list, stdout=PIPE)
        output = proc.stdout.read()
        proc.stdout.close()
        output = output[:-1]
        self.output_data = output.decode('UTF-8')
        return self.output_data

    def parse_data(self, data):
        #not implemeted yet
        pass
