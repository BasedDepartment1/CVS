import filecmp
import time
import unittest
import os
import random
import shutil
from cvs.directory_difference import DirectoryDifference
# from cvs.dir_changes import DirectoryChanges
# from cvs.dir_changes import DirectoryChanges


class DifferencesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.save_ = os.getcwd()

        os.mkdir("first_directory")
        os.chdir(self.save_ + "\\first_directory")
        os.mkdir("subdirectory1")

        os.chdir(self.save_)
        os.mkdir("second_directory")
        os.chdir(self.save_ + "\\second_directory")
        os.mkdir("subdirectory1")

        os.chdir(self.save_)

        self.dir1 = os.getcwd() + "\\first_directory"
        self.dir2 = os.getcwd() + "\\second_directory"
        self.subdir1 = self.dir1 + "\\subdirectory1"
        self.subdir2 = self.dir2 + "\\subdirectory1"
        self.trash = DirectoryDifference(self.dir1, self.dir2)

        os.chdir(self.save_)

    def tearDown(self) -> None:
        shutil.rmtree(self.dir1)
        shutil.rmtree(self.dir2)

    # def assert_orderless(self, expected):
    #     for element in expected:
    #         self.assertIn(element, self.trash.__find_directory_difference())
    #
    #     for element in self.trash.__find_directory_difference():
    #         self.assertIn(element, expected)

    def test_root_directory(self):
        time.sleep(1)
        with open(f"{self.dir1}\\testFile1.txt", "w+", encoding='utf-8',
                  errors='ignore') as f1:
            f1.write("123")

        with open(f"{self.dir2}\\testFile1.txt", "w+", encoding='utf-8',
                  errors='ignore') as f1:
            f1.write("321")

        expected = {
            "modified": [r"testFile1.txt"],
            "deleted": [],
            "new file": [],
        }
        self.assertDictEqual(expected, self.trash.changed_files)

        # expected = [
        #     DirectoryChanges(self.dir1, self.dir2)
        # ]
        # self.assert_orderless(expected)
    #
    # def test_sub_directories(self):
    #     time.sleep(1)
    #     with open(f"{self.subdir1}\\testFile1.txt", "w+", encoding='utf-8',
    #               errors='ignore') as f1:
    #         f1.write("3221")
    #
    #     with open(f"{self.subdir2}\\testFile1.txt", "w+", encoding='utf-8',
    #               errors='ignore') as f1:
    #         f1.write("3212")
    #
    #     expected = [
    #         DirectoryChanges(self.subdir1, self.subdir2)
    #     ]
    #
    #     self.assert_orderless(expected)


if __name__ == '__main__':
    unittest.main()
