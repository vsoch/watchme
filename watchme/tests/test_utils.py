#!/usr/bin/python

# Copyright (C) 2019 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittest.mock import patch
import unittest
import tempfile
import shutil
import json
from sys import platform
import os


print("############################################################ test_utils")

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.tmpdir)
        

    def test_write_read_files(self):
        '''test_write_read_files will test the functions write_file and read_file
        '''
        print("Testing utils.write_file")
        from watchme.utils import write_file
        import json
        tmpfile = tempfile.mkstemp()[1]
        os.remove(tmpfile)
        write_file(tmpfile,"mocos!")
        self.assertTrue(os.path.exists(tmpfile))        

        print("Testing utils.read_file...")
        from watchme.utils import read_file
        content = read_file(tmpfile)[0]
        self.assertEqual("mocos!", content)

        from watchme.utils import write_json
        print("Testing utils.write_json.")
        print("...Case 1: Providing bad json")
        bad_json = {"IWuvWaffles?'}":[{True}, "2", 3]}
        tmpfile = tempfile.mkstemp()[1]
        os.remove(tmpfile)        
        with self.assertRaises(TypeError) as cm:
            write_json(bad_json, tmpfile)

        print("...Case 2: Providing good json")        
        good_json = {"IWuvWaffles!": [True, "2", 3]}
        tmpfile = tempfile.mkstemp()[1]
        os.remove(tmpfile)
        write_json(good_json,tmpfile)
        with open(tmpfile,'r') as filey:
            content = json.loads(filey.read())
        self.assertTrue(isinstance(content, dict))
        self.assertTrue("IWuvWaffles!" in content)

        print("Testing utils.print_json")
        from watchme.utils import print_json
        result=print_json({1:1})
        self.assertEqual('{\n    "1": 1\n}', result)

    def test_get_installdir(self):
        '''get install directory should return the base of where singularity
        is installed
        '''
        print("Testing utils.get_installdir")
        from watchme.utils import get_installdir
        whereami = get_installdir()
        print(whereami)
        self.assertTrue(whereami.endswith('watchme'))

    def test_prompts(self):
        '''test user inputs and prompts'''
        from watchme.utils import confirm_prompt

        print('Testing utils.confirm_prompt')
        user_input = [
            'Y',
            'y',
            'n',
            'N',
        ]
        expected_responses = [
             True,
             True,
             False,
             False
        ]
        for i in range(len(user_input)):
            with patch('builtins.input', side_effect=user_input[i]):
                response = confirm_prompt("Please confirm this thing.")
            self.assertEqual(response, expected_responses[i])

    def test_terminal(self):

        print('Testing utils.run_command')
        from watchme.utils import run_command
        from watchme.utils import which
        result = run_command('echo Las Papas Fritas')
        self.assertEqual(result['message'], 'Las Papas Fritas\n')
        self.assertEqual(result['return_code'], 0)     

        print('Testing utils.which')
        result = which('echo')
        self.assertEqual(result, '/bin/echo')

    def test_userhome(self):
        print('Testing utils.get_user')
        print('Testing utils.get_userhome')
        from watchme.utils import get_userhome
        from watchme.utils import get_user
        user = get_user()
        userhome = get_userhome()
        print("Userhome is %s" % userhome)
        if platform.startswith("linux"):
            self.assertEqual('/home/%s' % user, userhome)
        elif platform == "darwin":
            self.assertEqual('/Users/%s' % user, userhome)

    def test_files(self):
        print('Testing utils.generate_temporary_files')
        from watchme.utils import generate_temporary_file

        tmpfile = generate_temporary_file()
        from watchme.utils import run_command
        run_command('touch %s' %tmpfile)
        print('Testing utils.copyfile')
        from watchme.utils import copyfile
        copyfile(tmpfile, '%s.booga' % tmpfile)
        self.assertTrue(os.path.exists('%s.booga' %tmpfile))
        self.assertTrue(os.path.exists(tmpfile))
        os.remove(tmpfile)
        os.remove("%s.booga" % tmpfile) 

    def test_mkdir(self):
        print('Testing utils.mkdir_p')
        from watchme.utils import mkdir_p
        tmpdir = os.path.join(self.tmpdir, "if", "I", "were", "an", "avocado")
        mkdir_p(tmpdir)
        self.assertTrue(os.path.exists(tmpdir))

        print('Testing utils.get_tmpdir')
        from watchme.utils import get_tmpdir
        tmpdir = get_tmpdir()
        self.assertTrue(os.path.exists(tmpdir))
        self.assertTrue('watchme' in tmpdir)
        shutil.rmtree(tmpdir)


if __name__ == '__main__':
    unittest.main()
