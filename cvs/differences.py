import itertools
import os
from typing import Dict, List, Any

from cvs.dir_changes import DirectoryChanges
from filecmp import dircmp


class Differences:
    """
    All changed files between two directories

    Attributes:
        dir_previous    Previous condition of directory.
        dir_current     Current condition of directory.
        changed_files   Dictionary with lists of added, deleted
                        and modified files.
    """

    def __init__(self, dir1: str, dir2: str):
        # self.sub_folders1 = [dir1, *find_all_sub_folders(dir1)]
        # self.sub_folders2 = [dir2, *find_all_sub_folders(dir2)]
        self.dir_previous = dir1
        # self.subdirs1 = find_all_directories(dir1)
        self.dir_current = dir2
        # self.dir_compared = filecmp.dircmp(self.dir1, self.dir2)
        self.changed_files = {
            "modified": [],
            "deleted": [],
            "new file": [],
        }
        self.__find_directory_difference(dircmp(self.dir_previous,
                                                self.dir_current))

    # def __find_directory_sub_folders(self) -> tuple[set, set]:
    # """
    # Finds all subfolders in main directories to analyze their difference
    # :return: Folders of previous and current directory
    # """
    # folders_prev = set()
    # folders_curr = set()
    # for dir_path, *_ in os.walk(self.dir_previous):
    #     folders_prev.add(dir_path[len(self.dir_previous):])
    # for dir_path, *_ in os.walk(self.dir_current):
    #     folders_curr.add(dir_path[len(self.dir_current):])
    #
    # return folders_prev, folders_curr

    @staticmethod
    def __get_files(c, dirs, filenames):
        return list(map(lambda x: os.path.join(c, x), filenames))

    def __find_directory_difference(self, dir_cmp: dircmp, prev_dir=None):
        if prev_dir is None:
            prev_dir = list()

        bias = '/'.join(prev_dir) + '/' if len(prev_dir) > 0 else ''
        for common_diff_file in dir_cmp.diff_files:
            self.changed_files["modified"].append(bias + common_diff_file)

        for deleted_file in dir_cmp.left_only:
            self.changed_files["deleted"].append(bias + deleted_file)
            path = f"{self.dir_previous}/{bias}{deleted_file}"
            if os.path.isdir(path):
                for file in itertools.chain.from_iterable(itertools.starmap(
                        self.__get_files, os.walk(path))):
                    self.changed_files["deleted"].append(
                        file[len(self.dir_previous) + 1:].replace("\\", "/")
                    )

        for new_file in dir_cmp.right_only:
            self.changed_files["new file"].append(bias + new_file)
            path = f"{self.dir_current}/{bias}{new_file}"
            if os.path.isdir(path):
                for file in itertools.chain.from_iterable(itertools.starmap(
                        self.__get_files, os.walk(path))):
                    self.changed_files["new file"].append(
                        file[len(self.dir_current) + 1:].replace("\\", "/")
                    )

        for subdir, subdir_cmp in dir_cmp.subdirs.items():
            self.__find_directory_difference(subdir_cmp, [*prev_dir, subdir])
        # """
        # Finds difference between two directories
        # :return: List of differences between each of subfolders
        # """
        # prev_folders, curr_folders = self.__find_directory_sub_folders()
        # difference = []
        #
        # for directory in prev_folders.intersection(curr_folders):
        #     difference.append(DirectoryChanges(
        #         f"{self.dir_previous}{directory}",
        #         f"{self.dir_current}{directory}"
        #     ))
        # for directory in prev_folders.difference(curr_folders):
        #     difference.append(DirectoryChanges(
        #         dir_prev=f"{self.dir_previous}{directory}"
        #     ))
        # for directory in curr_folders.difference(prev_folders):
        #     difference.append(DirectoryChanges(
        #         dir_current=f"{self.dir_current}{directory}"
        #     ))
        #
        # return list(filter(lambda ch: len(ch.file_changes) != 0, difference))

    # @staticmethod
    # def __get_current_directory_files(directory) -> list:
    #     for *dir_info, filenames in os.walk(directory):
    #         return filenames
    #
    # def __find_subdirectory_difference(self, subdir1, subdir2):
    #     sub_dirs_compared = filecmp.dircmp(subdir1, subdir2)
    #     dir1_files = self.__get_current_directory_files(subdir1)
    #     dir2_files = self.__get_current_directory_files(subdir2)

    def __str__(self):
        dif_file_ins = []
        for cat, files in self.changed_files.items():
            for file in files:
                dif_file_ins.append(f"{cat}:\t{file}")
        return '\n'.join(dif_file_ins)


if __name__ == "__main__":
    pass
