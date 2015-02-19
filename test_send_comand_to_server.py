#!/usr/bin/env python3
''' This program makes test of program send_comand_to_server. '''

import unittest
from send_comand_to_server import SshDataGetter as SDG

class TestSShDataGetter(unittest.TestCase):
    ''' Class of test. '''
    message = 'was: {}, should: {}'
    string = "telnet -c 'echo xx' username ip password"
    words = ["telnet", "-c", "username", "ip", "password", "echo xx"]
    my_ip = '127.0.0.1'
    my_username = 'maria'
    my_comand = 'echo it works!'
    output_data = 'it works!'

    def test_split_to_values(self):
        ''' Method makes a test of split_to_values in
            send_comand_to_server.py.
        '''
        sdg_object = SDG()
        result = sdg_object.split_to_values(self.string)
        assert result == self.words, self.message.format(result, self.words)

    def test_get_values(self):
        ''' Method makes tests of get_values in send_comand_to_server.py. '''
        sdg_object = SDG()
        sdg_object.get_values(self.string)
        assert sdg_object.username == self.words[2], self.message.format(
            sdg_object.username, self.words[2]
            )
        assert sdg_object.ip == self.words[3], self.message.format(
            sdg_object.ip, self.words[3]
            )
        assert sdg_object.password == self.words[4], self.message.format(
            sdg_object.password, self.words[4]
            )
        assert sdg_object.comand == self.words[5], self.message.format(
            sdg_object.comand, self.words[5]
            )

    def test(self):
        sdg_object = SDG()
        sdg_object.comand = self.my_comand
        sdg_object.get_my_data()
        result = sdg_object.get_data()

        assert result == self.output_data, self.message.format(
            result, self.output_data
            )

if __name__ == '__main__':
    unittest.main()
