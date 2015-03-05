#!/usr/bin/env python3
''' This program makes test of program send_command_to_server. '''

import unittest
from send_command_to_server import SshDataGetter as SshGetter

class TestSShDataGetter(unittest.TestCase):
    ''' Class of test. '''
    string = "telnet -c 'echo xx' username ip_address password"
    words = ["telnet", "-c", "username", "ip_address", "password", "echo xx"]
    my_command = 'echo it works!'
    my_output_data = 'it works!'

    def test_split_to_values(self):
        ''' Method makes a test of split_to_values in
            send_command_to_server.py.
        '''
        ssh_getter = SshGetter()
        list_of_values = ssh_getter.split_to_values(self.string)

        self.assertEqual(list_of_values, self.words)

    def test_get_values(self):
        ''' Method makes tests of get_values in send_command_to_server.py. '''
        ssh_getter = SshGetter()
        ssh_getter.get_values(self.string)

        self.assertEqual(ssh_getter.username, self.words[2])
        self.assertEqual(ssh_getter.ip_address, self.words[3])
        self.assertEqual(ssh_getter.password, self.words[4])
        self.assertEqual(ssh_getter.command, self.words[5])

    def test_get_data(self):
        ''' Method makes test of get_data in send_command_to_server.py. '''
        ssh_getter = SshGetter()
        #TODO: Enter you data in empty strings lower
        ssh_getter.ip_address = '' #your ip address
        ssh_getter.username = '' #your username
        ssh_getter.password = '' #your password
        ssh_getter.command = self.my_command
        command_output = ssh_getter.get_data()

        self.assertEqual(command_output, self.my_output_data)

if __name__ == '__main__':
    unittest.main()
