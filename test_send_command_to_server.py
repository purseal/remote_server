#!/usr/bin/env python3
''' This program makes test of program send_command_to_server. '''

import unittest
from send_comand_to_server import SshDataGetter as SDG

class TestSShDataGetter(unittest.TestCase):
    ''' Class of test. '''
    message = 'was: {}, should: {}'
    string = "telnet -c 'echo xx' username ip_address password"
    words = ["telnet", "-c", "username", "ip_address", "password", "echo xx"]
    my_ip_address = '127.0.0.1'
    my_username = 'maria'
    my_command = 'echo it works!'
    output_data = 'it works!'

    def test_split_to_values(self):
        ''' Method makes a test of split_to_values in
            send_command_to_server.py.
        '''
        sdg_object = SDG()
        result = sdg_object.split_to_values(self.string)

        assert result == self.words, self.message.format(result, self.words)

    def test_get_values(self):
        ''' Method makes tests of get_values in send_command_to_server.py. '''
        sdg_object = SDG()
        sdg_object.get_values(self.string)

        assert sdg_object.username == self.words[2], self.message.format(
            sdg_object.username, self.words[2]
            )
        assert sdg_object.ip_address == self.words[3], self.message.format(
            sdg_object.ip_address, self.words[3]
            )
        assert sdg_object.password == self.words[4], self.message.format(
            sdg_object.password, self.words[4]
            )
        assert sdg_object.command == self.words[5], self.message.format(
            sdg_object.command, self.words[5]
            )

    def test_get_data(self):
        ''' Method makes test of get_data in send_command_to_server.py. '''
        my_file = open('/home/maria/prog/my_data', 'r')
        sdg_object = SDG()
        data = my_file.readlines()
        sdg_object.ip_address = data[1]
        sdg_object.username = data[2]
        sdg_object.password = data[0]
        sdg_object.command = self.my_command
        my_file.close()
        result = sdg_object.get_data()

        assert result == self.output_data, self.message.format(
            result, self.output_data
            )

if __name__ == '__main__':
    unittest.main()
