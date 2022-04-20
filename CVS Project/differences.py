import filecmp
import difflib
import unittest
import os
import random
import shutil

# TODO мб это по разным файлам раскидать


class Differences:
    """
    Stores all changes between directories
    """

    def __init__(self, dir1: str, dir2: str):
        # self.sub_folders1 = [dir1, *find_all_sub_folders(dir1)]
        # self.sub_folders2 = [dir2, *find_all_sub_folders(dir2)]
        self.dir_previous = dir1
        # self.subdirs1 = find_all_directories(dir1)
        self.dir_current = dir2
        # self.dir_compared = filecmp.dircmp(self.dir1, self.dir2)

    # def __find_all_sub_folders(self, dirname: str) -> list[str]:
    #     sub_folders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    #     for dirname in list(sub_folders):
    #         sub_folders.extend(self.__find_all_sub_folders(dirname))
    #     return sub_folders

    def __find_directory_sub_folders(self) -> tuple[set, set]:
        """
        Finds all subfolders in main directories to analyze their difference
        :return: Folders of previous and current directory
        """
        folders_prev = set()
        folders_curr = set()
        for dir_path, *_ in os.walk(self.dir_previous):
            folders_prev.add(dir_path)
        for dir_path, *_ in os.walk(self.dir_current):
            folders_curr.add(dir_path)
        return folders_prev, folders_curr

    def directory_difference(self):
        """
        Finds difference between two directories
        :return: List of differences between each of subfolders
        """
        prev_folders, curr_folders = self.__find_directory_sub_folders()
        difference = []
        for directory in prev_folders.intersection(curr_folders):
            difference.append(DirectoryChanges(
                f"{self.dir_previous}\\{directory}",
                f"{self.dir_current}\\{directory}"
            ))
        for directory in prev_folders.difference(curr_folders):
            difference.append(DirectoryChanges(
                dir_prev=f"{self.dir_previous}\\{directory}"
            ))
        for directory in curr_folders.difference(prev_folders):
            difference.append(DirectoryChanges(
                dir_current=f"{self.dir_current}\\{directory}"
            ))
        return difference

    # @staticmethod
    # def __get_current_directory_files(directory) -> list:
    #     for *dir_info, filenames in os.walk(directory):
    #         return filenames
    #
    # def __find_subdirectory_difference(self, subdir1, subdir2):
    #     sub_dirs_compared = filecmp.dircmp(subdir1, subdir2)
    #     dir1_files = self.__get_current_directory_files(subdir1)
    #     dir2_files = self.__get_current_directory_files(subdir2)


class DirectoryChanges:
    """
    Stores all information about difference between files of two directories
    """
    def __init__(self, dir_prev: str = None, dir_current: str = None):
        self.path = dir_current

        self.__prev = dir_prev
        self.__current = dir_current

        self.file_changes = []
        self.__find_non_common_file_difference()

        if dir_prev is not None and dir_current is not None:
            self.__find_common_file_difference()

    @staticmethod
    def __get_current_directory_files(directory) -> set:
        if directory is None:
            return set()
        for *dir_info, filenames in os.walk(directory):
            return set(filenames)

    def __find_common_file_difference(self):
        """
        Finds difference between fies that exist in both directories
        """
        dirs_compared = filecmp.dircmp(self.__prev, self.__current)
        for file_name in dirs_compared.diff_files:
            previous_path = f'{self.__prev}\\{file_name}'
            current_path = f'{self.__current}\\{file_name}'
            self.file_changes\
                .append(FileChanges(previous_path, current_path))

    def __find_non_common_file_difference(self):
        """
        Creates information about deleted and added files
        """
        dir1_files = self.__get_current_directory_files(self.__prev)
        dir2_files = self.__get_current_directory_files(self.__current)
        deleted_files = dir1_files.difference(dir2_files)
        created_files = dir2_files.difference(dir1_files)
        for file in deleted_files:
            path = f'{self.__prev}\\{file}'
            self.file_changes.append(FileChanges(path))
        for file in created_files:
            path = f'{self.__current}\\{file}'
            self.file_changes.append(FileChanges(None, path))


class FileChanges:
    """
    Stores all information about difference between two files
    """
    def __init__(self, prev_file_path: str = None,
                 curr_file_path: str = None):
        if prev_file_path is not None:
            with open(prev_file_path, 'r', encoding='utf-8') as f1:
                self.__file_lines_1 = f1.readlines()
        else:
            self.__file_lines_1 = []

        if curr_file_path is not None:
            with open(curr_file_path, 'r', encoding='utf-8') as f2:
                self.__file_lines_2 = f2.readlines()
        else:
            self.__file_lines_2 = []
        self.file_path = curr_file_path
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

    def test_when_on_empty_file(self):
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
