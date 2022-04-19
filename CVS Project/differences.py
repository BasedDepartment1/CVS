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

    def __init__(self, dir1: str, dir2: str):
        self.dir1 = dir1
        self.dir2 = dir2
        self.dir_compared = filecmp.dircmp(self.dir1, self.dir2)


class Changes:
    """
    All connected with changes
    """

    def __init__(self, prev_file_path: str = None,
                 curr_file_path: str = None):
        if prev_file_path is not None:
            with open(prev_file_path,
                      'r',
                      encoding='utf-8',
                      errors='ignore') \
                    as f1:
                self.__file_lines_1 = f1.readlines()
        else:
            self.__file_lines_1 = []

        if curr_file_path is not None:
            with open(curr_file_path,
                      'r',
                      encoding='utf-8',
                      errors='ignore') \
                    as f2:
                self.__file_lines_2 = f2.readlines()
        else:
            self.__file_lines_2 = []
        self.changes = self.find_difference(self.__file_lines_1,
                                            self.__file_lines_2)

    @staticmethod
    def find_difference(lines1, lines2):
        differ = difflib.Differ()
        differences = list(differ.compare(lines1, lines2))
        diff_counter = 0
        diff_started = False
        full_changes_dto = []
        for line in filter(lambda c: c[0] != "?", differences):
            if line[0] == "-":
                diff_started = True
                full_changes_dto.append(DifferenceDTO(line[2:], None,
                                                      diff_counter))
            elif line[0] == "+":
                if diff_started:
                    full_changes_dto[-1].added = line[2:]
                    diff_counter -= 1
                    diff_started = False
                else:
                    full_changes_dto.append(DifferenceDTO(None, line[2:],
                                                          diff_counter))
            diff_counter += 1
        return full_changes_dto


class DifferenceDTO:
    def __init__(self, removed: str | None, added: str | None, index: int):
        self.removed = removed
        self.added = added
        self.index = index

    def __eq__(self, other: "DifferenceDTO"):
        return self.removed == other.removed \
               and self.added == other.added \
               and self.index == other.index

    def __str__(self):
        return f"{self.index} - {self.removed}\n" \
               f"{len(str(self.index)) * ' '} + {self.added}"

    def __repr__(self):
        return f"DifferenceDTO({self.removed, self.added, self.index})"


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
        trash = Changes()
        f1 = ["first line", "second line", "third line"]
        f2 = ["first line", "second line", "difference"]
        actual_changes = trash.find_difference(f1, f2)
        expected_changes = [DifferenceDTO("third line", "difference", 2)]
        self.assertListEqual(expected_changes, actual_changes)

    def test_when_extra_line_difference_finder(self):
        trash = Changes()
        f1 = ["first line", "odd", "second line", "third line"]
        f2 = ["first line", "second line", "difference"]
        actual_changes = trash.find_difference(f1, f2)
        expected_changes = [DifferenceDTO("odd", None, 1),
                            DifferenceDTO("third line", "difference", 3)]
        self.assertListEqual(expected_changes, actual_changes)

    def test_when_question_mark(self):
        trash = Changes()
        f1 = ["f?rst line", "second line", "third line"]
        f2 = ["first line", "second line", "difference"]
        actual_changes = trash.find_difference(f1, f2)
        expected_changes = [DifferenceDTO("f?rst line", "first line", 0),
                            DifferenceDTO("third line", "difference", 2)]
        self.assertListEqual(expected_changes, actual_changes)

    def test_complex_find_differences(self):
        trash = Changes()
        f1 = ["f+rst line", "second line", "third line"]
        f2 = ["first line", "odd", "second line", "difference"]
        actual_changes = trash.find_difference(f1, f2)
        expected_changes = [DifferenceDTO("f+rst line", "first line", 0),
                            DifferenceDTO(None, "odd", 1),
                            DifferenceDTO("third line", "difference", 3)]
        self.assertListEqual(expected_changes, actual_changes)

    def test_when_on_empty_file(self):
        trash = Changes()
        f1 = ["f+rst line"]
        f2 = []
        actual_changes = trash.find_difference(f1, f2)
        expected_changes = [DifferenceDTO("f+rst line", None, 0)]

        self.assertListEqual(expected_changes, actual_changes)

        actual_changes = trash.find_difference(f2, f1)
        expected_changes = [DifferenceDTO(None, "f+rst line", 0)]

        self.assertEqual(expected_changes, actual_changes)



