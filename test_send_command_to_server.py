#!/usr/bin/env python3
#pylint: disable=too-many-public-methods

''' This program makes test of program send_command_to_server. '''

import unittest
from send_command_to_server import SshDataGetter as SshGetter

class TestSShDataGetter(unittest.TestCase):
    ''' Class of test. '''
    string = "ssh -c 'echo xx' username ip_address password"
    words = ["ssh", "-c", "username", "ip_address", "password", "echo xx"]
    my_command = 'echo it works!'
    my_output_data = 'it works!'
    my_wrong_command = 'echoo it works!'
    my_error_message = '''bash: echoo: command not found'''
    output = '- [16:39:09]maria~$:echo it works!\n- it works!'
    output_with_volume_gb = 'param1: 15.4GB 32.4'
    output_with_volume_mb = 'param1: 15.4MB 32.4'
    required_volume_gb = '15.4GB'
    required_volume_mb = '15.4MB'
    volumes = '15.4GB 14.0GB'
    required_volumes = [('15.4', 'GB'), ('14.0', 'GB')]
    volumes_gb_mb = '15.4GB 30.0MB'
    required_volume_gb_mb = '15.43GB'
    server_volume = '35900.0GB'
    sensor_status_output = "1-Ctlr A 55 C OK\n1-Ctlr B 54  C OK"
    required_sensor_status_output = {"1-Ctlr A" : '55 C', '1-Ctlr B' : '54  C'}
    output_of_disk_helth = "0.0  SN  Vendor  rev  VDISK  SAS  146.1GB  3.0  "
    output_of_disk_helth += "OK"
    disk_helth = {"0.0" : "OK"}
    server_disks_helth = {'0.0' : 'OK'}
    server_current_volume = '356.7GB'

    def test_split_to_values(self):
        '''
            Method makes a test of split_to_values in
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
        #Enter you data in empty strings lower.
        ssh_getter.ip_address = '127.0.0.1' #your ip address
        ssh_getter.username = 'maria' #your username
        ssh_getter.password = 'Lubitleto' #your password
        ssh_getter.command = self.my_command
        command_output = ssh_getter.get_output()

        self.assertEqual(command_output, self.my_output_data)

        ssh_getter.command = self.my_wrong_command
        command_output = ssh_getter.get_output()

        self.assertEqual(command_output, self.my_error_message)

    def test_parse_output(self):
        '''
            Method makes test of parse_output in send_command_to_server.py.
        '''
        ssh_getter = SshGetter()
        ssh_getter.output_data = self.output
        ssh_getter.command = self.my_command
        analyzed_output = ssh_getter.parse_output()

        self.assertEqual(analyzed_output, self.my_output_data)

    def test_parse_all_volumes(self):
        '''
            Method makes test of parse_volumes in send_command_to_server.py.
        '''
        ssh_getter = SshGetter()
        ssh_getter.output_data = self.volumes
        analyzed_output = ssh_getter.parse_all_volumes()

        self.assertEqual(analyzed_output, self.required_volumes)

        ssh_getter.output_data = self.sensor_status_output
        analyzed_output = ssh_getter.parse_all_volumes()

        self.assertEqual(analyzed_output, None)

    def test_parse_total_volume(self):
        '''
            Method makes test of get_total_volume in send_command_to_server.py.
        '''
        ssh_getter = SshGetter()
        ssh_getter.output_data = self.volumes_gb_mb
        analyzed_output = ssh_getter.parse_total_volume()

        self.assertEqual(analyzed_output, self.required_volume_gb_mb)

    def test_parse_current_volume(self):
        ssh_getter = SshGetter()
        ssh_getter.output_data = self.volumes_gb_mb
        analyzed_output = ssh_getter.parse_current_volume(0)

        self.assertEqual(analyzed_output, self.required_volume_gb)


    def test_parse_temperature(self):
        '''
            Method makes test of parse_temperature in send_command_to_server.py.
        '''
        ssh_getter = SshGetter()
        ssh_getter.output_data = self.sensor_status_output
        analyzed_output = ssh_getter.parse_temperature()

        self.assertEqual(analyzed_output, self.required_sensor_status_output)

    def test_parse_disks_helth(self):
        '''
            Method makes test of parse_disk_helth in send_command_to_server.py.
        '''
        ssh_getter = SshGetter()
        ssh_getter.output_data = self.output_of_disk_helth
        analyzed_output = ssh_getter.parse_disks_helth()

        self.assertEqual(analyzed_output, self.disk_helth)

#TODO: delete # below to test prog on server
 #  def test_get_temperature(self):
 #      '''
 #          Method makes test of get_temperature in send_command_to_server.py.
 #      '''
 #      ssh_getter = SshGetter()
 #      ssh_getter.ip_address = "10.1.5.1"
 #      ssh_getter.password = "!manage"
 #      ssh_getter.username = "manage"
 #      ssh_getter.command = "show sensor-status"
 #      analyzed_output = ssh_getter.get_temperature()

 #      self.assertEqual(analyzed_output, self.required_sensor_status_output)

 #  def test_get_volume(self):
 #      '''
 #          Method makes test of get_volume in send_command_to_server.py.
 #      '''
 #      ssh_getter = SshGetter()
 #      ssh_getter.ip_address = "10.1.5.1"
 #      ssh_getter.password = "!manage"
 #      ssh_getter.username = "manage"
 #      ssh_getter.command = "show volumes"
 #      analyzed_output = ssh_getter.get_total_volume()

 #      self.assertEqual(analyzed_output, self.server_volume)

 #  def test_get_disk_helth(self):
 #      '''
 #          Method makes test of get_disks_helth in send_command_to_server.py.
 #      '''
 #      ssh_getter = SshGetter()
 #      ssh_getter.ip_address = "10.1.5.1"
 #      ssh_getter.password = "!manage"
 #      ssh_getter.username = "manage"
 #      ssh_getter.command = "show disks"
 #      analyzed_output = ssh_getter.get_disks_helth()

 #      self.assertEqual(analyzed_output, self.server_disks_helth)

 #  def test_get_current_volume(self):
 #      '''
 #          Method makes test of get_current_volume in send_command_to_server.py.
 #      '''
 #      ssh_getter = SshGetter()
 #      ssh_getter.ip_address = "10.1.5.1"
 #      ssh_getter.password = "!manage"
 #      ssh_getter.username = "manage"
 #      ssh_getter.command = "show disks"
 #      analyzed_output = ssh_getter.get_currnet_volume(0)

 #      self.assertEqual(analyzed_output, self.server_current_volume)

if __name__ == '__main__':
    unittest.main()
