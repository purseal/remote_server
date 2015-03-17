#!/usr/bin/env python3
''' This program makes test of program send_command_to_server. '''

import unittest
from send_command_to_server import SshDataGetter as SshGetter

class TestSShDataGetter(unittest.TestCase):
    ''' Class of test. '''
    string = "telnet -c 'echo xx' username ip_address password"
    words = ["telnet", "-c", "username", "ip_address", "password", "echo xx"]
    my_command = 'echo param1:__15.4 MBIS 2'
    my_output = 'param1:__15.4 MBIS 2'
    out = '15 4'
    expected_analyzed_output = '15.4'

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

    def test_get_output(self):
        ''' Method makes test of get_data in send_command_to_server.py. '''
        ssh_getter = SshGetter()
        #TODO: Enter you data in empty strings lower.
        ssh_getter.ip_address = '' #your ip address
        ssh_getter.username = '' #your username
        ssh_getter.password = '' #your password
        ssh_getter.command = self.my_command
        command_output = ssh_getter.get_output()

        self.assertEqual(command_output, self.my_output)

    def test_parse_output(self):
        ''' Method makes test of parse_output in send_command_to_server.py. '''
        ssh_getter = SshGetter()
        ssh_getter.output_data = self.out
        analyzed_output = ssh_getter.parse_output()

        self.assertEqual(analyzed_output, None)

        ssh_getter.output_data = self.my_output
        analyzed_output = ssh_getter.parse_output()

        self.assertEqual(analyzed_output, self.expected_analyzed_output)


if __name__ == '__main__':
    unittest.main()
