import filecmp
import difflib
import unittest
import os
import random
import shutil


class Differences:
    """
    Stores all changes between directories
    """
    pass


class DifferencesTests(unittest.TestCase):
    def setUp(self) -> None:
        os.mkdir("first_directory")
        os.mkdir("second_directory")
        self.dir1 = os.getcwd() + "\\first_directory"
        self.dir2 = os.getcwd() + "\\second_directory"

    def tearDown(self) -> None:
        shutil.rmtree(self.dir1)
        shutil.rmtree(self.dir2)

    def test_certainly_not_equal(self):
        a = filecmp.dircmp(self.dir1, self.dir2, ignore=None, hide=None)
        for i in range(20):
            with open(f"{self.dir1}\\testFile{i}.txt", "w+", encoding='utf-8',
                      errors='ignore') as f:
                f.write(str(random.randint(1, 100)))

        for i in range(20):
            with open(f"{self.dir2}\\testFile{i}.txt", "w+", encoding='utf-8',
                      errors='ignore') as f:
                f.write(str(random.randint(101, 200)))
        same_files = a.same_files.copy()
        self.assertEqual(len(same_files), 0, msg="Something has gone wrong!")

        # common = a.common_files
        # dif = a.diff_files

        # all_files_in_dir1 = set(file.name for file in os.scandir(self.dir1))
        # all_files_in_dir2 = set(file.name for file in os.scandir(self.dir2))

        # print(all_files_in_dir1.difference(all_files_in_dir2))
        # print(all_files_in_dir2.difference(all_files_in_dir1))

        # di = difflib.Differ()
        # res = di.compare(lines_for_file_1, lines_for_file_2)
        # print("".join(res))
