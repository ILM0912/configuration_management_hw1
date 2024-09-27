import os
import shutil
import unittest

import main
from main import command_cd, command_ls, command_touch, command_mv, command_tac, command_find


class TestShellCommands(unittest.TestCase):

    def setUp(self):
        main.disk_files = 'test_dir.tar'
        main.GUI()
        os.remove("test_dir.tar")
        shutil.copy("first_state_disk.tar", "test_dir.tar")

    # tests for ls
    def test_ls_empty__dir_folder_1(self):
        main.current_dir = 'disk/folder_1/'
        self.assertEqual(command_ls(""), 'a1.txt\n'
                                         'b1.txt\n'
                                         'inside_folder\n')

    def test_ls_2dot__dir_disk(self):
        main.current_dir = 'disk/'
        self.assertEqual(command_ls(".."), 'disk\n')

    def test_ls_2dotAndSlash__dir_disk(self):
        main.current_dir = 'disk/'
        self.assertEqual(command_ls("../folder_1"), 'a1.txt\n'
                                                    'b1.txt\n'
                                                    'inside_folder\n')

    def test_ls_abspath_empty_folder(self):
        main.current_dir = 'disk/'
        self.assertEqual(command_ls("/disk/folder_3"), 'Directory is empty\n')

    # tests for cd
    def test_cd_empty__dir_folder_1(self):
        main.current_dir = 'disk/folder_1/'
        self.assertEqual(command_cd(""), 'disk/folder_1/\n')

    def test_cd_2dot__dir_disk(self):
        main.current_dir = 'disk/'
        self.assertEqual(command_cd(".."), 'already in disk')

    def test_cd_2dotAndSlash__dir_disk(self):
        main.GUI()
        main.current_dir = 'disk/'
        self.assertEqual(command_cd("../folder_1"), 'disk/folder_1/')

    def test_cd_no_such_dir(self):
        main.current_dir = 'disk/'
        self.assertEqual(command_cd("/disk/folder_4"), 'No such directory: /disk/folder_4\n')

    # tests for touch
    def test_touch_file_exist(self):
        main.current_dir = 'disk/folder_1/'
        self.assertEqual(command_touch("a1.txt"), 'File already exists: disk/folder_1/a1.txt\n')

    def test_touch_not_file(self):
        main.current_dir = 'disk/'
        self.assertEqual(command_touch("text."), 'It is not a file: disk/text.\n')

    def test_touch_success(self):
        main.current_dir = 'disk/'
        self.assertEqual(command_touch("text_4.txt"), 'file created disk/text_4.txt')

    # tests for tac
    def test_tac_file_dont_exist(self):
        main.current_dir = 'disk/folder_1/'
        self.assertEqual(command_tac(["a1."]), 'No such file: disk/folder_1/a1.\n\n')

    def test_tac_success(self):
        main.current_dir = 'disk/'
        self.assertEqual(command_tac(["text_1.txt"]), 'file: disk/text_1.txt\n'
                                                      'five\n'
                                                      'four\n'
                                                      'three\n'
                                                      'two\n'
                                                      'one\n\n')

    # tests for mv
    def test_mv_source_file_dont_exist(self):
        main.current_dir = 'disk/folder_1/'
        self.assertEqual(command_mv("a1.", ".."), 'Not files: disk/folder_1/a1. disk/a1.\n')

    def test_mv_success(self):
        main.current_dir = 'disk/'
        self.assertEqual(command_mv("text_1.txt", "./folder_2"), "disk/folder_2/text_1.txt")

    def test_mv_destination_no_dir(self):
        main.current_dir = 'disk/folder_1/'
        self.assertEqual(command_mv('a1.txt', 'folder'), 'No destination directory disk/folder_1/folder\n')

    def test_mv_same_name(self):
        main.current_dir = 'disk/folder_1/'
        self.assertEqual(command_mv('a1.txt', '~/'), 'disk/a1.txt')

    def test_mv_change_type(self):
        main.current_dir = 'disk/folder_1/'
        self.assertEqual(command_mv('a1.txt', 'a1.dhsj'), 'You can`t change file type disk/folder_1/a1.txt '
                                                          'disk/folder_1/a1.dhsj\n')

    # tests for find
    def test_find_all(self):
        main.current_dir = 'disk/folder_1/'
        self.assertEqual(command_find("-all", "*text*.*"), 'disk/folder_1/inside_folder/inside_text.txt\n'
                                                           'disk/text_1.txt\n'
                                                           'disk/text_2.txt\n'
                                                           'disk/text_3.txt\n')

    def test_find_in_dir(self):
        main.current_dir = 'disk/'
        self.assertEqual(command_find("folder_1", "?1.txt"), "disk/folder_1/a1.txt\n"
                                                             "disk/folder_1/b1.txt\n")

    def test_find_not_files(self):
        main.current_dir = 'disk/folder_1/'
        self.assertEqual(command_find('-all', 'folder'), 'I dont understand your mask: folder\n')

    def test_find_not_dir(self):
        main.current_dir = 'disk/'
        self.assertEqual(command_find('text_1.txt', '*.*'), 'Not a directory: disk/text_1.txt\n')

    def test_find_different_mask(self):
        main.current_dir = 'disk/folder_1/'
        self.assertEqual(command_find('-all', '??.*'), 'disk/folder_1/a1.txt\n'
                                                       'disk/folder_1/b1.txt\n'
                                                       'disk/folder_2/a2.txt\n'
                                                       'disk/folder_2/b2.txt\n')


if __name__ == "__main__":
    unittest.main()
