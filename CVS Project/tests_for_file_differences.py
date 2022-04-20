import filecmp
import unittest
import os
import random
import shutil
from data_transfer_objects import DifferenceDTO
from file_changes import FileChanges


class FileDifferencesTests(unittest.TestCase):
    def setUp(self) -> None:
        os.mkdir("first_directory")
        os.mkdir("second_directory")
        self.dir1 = os.getcwd() + "\\first_directory"
        self.dir2 = os.getcwd() + "\\second_directory"

    def tearDown(self) -> None:
        shutil.rmtree(self.dir1)
        shutil.rmtree(self.dir2)

    def test_certainly_not_equal(self):
        file_cmp = filecmp.dircmp(self.dir1, self.dir2, ignore=None, hide=None)
        for i in range(20):
            with open(f"{self.dir1}\\testFile{i}.txt", "w+", encoding='utf-8',
                      errors='ignore') as f:
                f.write(str(random.randint(1, 100)))

        for i in range(20):
            with open(f"{self.dir2}\\testFile{i}.txt", "w+", encoding='utf-8',
                      errors='ignore') as f:
                f.write(str(random.randint(101, 200)))
        same_files = file_cmp.same_files.copy()
        self.assertEqual(len(same_files), 0, msg="Something has gone wrong!")

    def test_simple_difference_finder(self):
        trash = FileChanges()
        f1 = ["first line", "second line", "third line"]
        f2 = ["first line", "second line", "difference"]
        actual_changes = trash.find_difference(f1, f2)
        expected_changes = [DifferenceDTO("third line", "difference", 2)]
        self.assertListEqual(expected_changes, actual_changes)

    def test_when_extra_line_difference_finder(self):
        trash = FileChanges()
        f1 = ["first line", "odd", "second line", "third line"]
        f2 = ["first line", "second line", "difference"]
        actual_changes = trash.find_difference(f1, f2)
        expected_changes = [DifferenceDTO("odd", None, 1),
                            DifferenceDTO("third line", "difference", 3)]
        self.assertListEqual(expected_changes, actual_changes)

    def test_when_question_mark(self):
        trash = FileChanges()
        f1 = ["f?rst line", "second line", "third line"]
        f2 = ["first line", "second line", "difference"]
        actual_changes = trash.find_difference(f1, f2)
        expected_changes = [DifferenceDTO("f?rst line", "first line", 0),
                            DifferenceDTO("third line", "difference", 2)]
        self.assertListEqual(expected_changes, actual_changes)

    def test_complex_find_differences(self):
        trash = FileChanges()
        f1 = ["f+rst line", "second line", "third line"]
        f2 = ["first line", "odd", "second line", "difference"]
        actual_changes = trash.find_difference(f1, f2)
        expected_changes = [DifferenceDTO("f+rst line", "first line", 0),
                            DifferenceDTO(None, "odd", 1),
                            DifferenceDTO("third line", "difference", 3)]
        self.assertListEqual(expected_changes, actual_changes)

    def test_on_empty_file_works_both_sides(self):
        trash = FileChanges()
        f1 = ["f+rst line"]
        f2 = []
        actual_changes = trash.find_difference(f1, f2)
        expected_changes = [DifferenceDTO("f+rst line", None, 0)]

        self.assertListEqual(expected_changes, actual_changes)

        actual_changes = trash.find_difference(f2, f1)
        expected_changes = [DifferenceDTO(None, "f+rst line", 0)]

        self.assertEqual(expected_changes, actual_changes)

        # TODO тесты тесты тесты тесты


if __name__ == '__main__':
    unittest.main()
