import filecmp
import unittest
import os
import random
import shutil
from data_transfer_objects import DifferenceDTO
from file_changes import FileChanges
from differences import Differences


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
        self.subdir = self.dir1 + "\\subdirectory1"

        os.chdir(self.save_)

    def tearDown(self) -> None:
        shutil.rmtree(self.dir1)
        shutil.rmtree(self.dir2)

    def test_something(self):
        with open(f"{self.dir1}\\testFile1.txt", "w+", encoding='utf-8',
                  errors='ignore') as f1:
            f1.write("123")

        with open(f"{self.dir2}\\testFile1.txt", "w+", encoding='utf-8',
                  errors='ignore') as f1:
            f1.write("321")

        with open(f"{self.subdir}\\testFile1.txt", "w+", encoding='utf-8',
                  errors='ignore') as f1:
            f1.write("3221")

        with open(f"{self.subdir}\\testFile1.txt", "w+", encoding='utf-8',
                  errors='ignore') as f1:
            f1.write("3212")

        trash = Differences(self.dir1, self.dir2)
        
        expected = []


if __name__ == '__main__':
    unittest.main()
