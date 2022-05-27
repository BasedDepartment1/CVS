import itertools
import os
from filecmp import dircmp
from enum import Enum


class DiffKeys(Enum):
    MODIFIED = "modified"
    DELETED = "deleted"
    NEW_FILE = "new file"


class DirectoryDifference:
    """
    All changed files between two directories

    Attributes:
        dir_previous    Previous condition of directory.
        dir_current     Current condition of directory.
        changed_files   Dictionary with lists of added, deleted
                        and modified files.
    """

    def __init__(self, dir1: str, dir2: str):
        self.dir_previous = dir1
        self.dir_current = dir2
        self.changed_files = {
            DiffKeys.MODIFIED: [],
            DiffKeys.DELETED: [],
            DiffKeys.NEW_FILE: [],
        }
        self.__find_directory_difference(dircmp(self.dir_previous,
                                                self.dir_current))

    @staticmethod
    def __get_files(c, dirs, filenames):
        return list(map(lambda x: os.path.join(c, x), filenames))

    def __find_directory_difference(self, dir_cmp: dircmp, prev_dir=None):
        if prev_dir is None:
            prev_dir = list()

        bias = '/'.join(prev_dir) + '/' if len(prev_dir) > 0 else ''
        for common_diff_file in dir_cmp.diff_files:
            self.changed_files[DiffKeys.MODIFIED]\
                .append(bias + common_diff_file)

        self.__add_to_changes(
            dir_cmp.left_only, DiffKeys.DELETED, self.dir_previous, bias)

        self.__add_to_changes(
            dir_cmp.right_only, DiffKeys.NEW_FILE, self.dir_current, bias)

        for subdir, subdir_cmp in dir_cmp.subdirs.items():
            self.__find_directory_difference(subdir_cmp, [*prev_dir, subdir])

    def __add_to_changes(self,
                         files: list,
                         key: DiffKeys,
                         directory: str,
                         bias: str
                         ):
        for unique_file in files:
            self.changed_files[key].append(bias + unique_file)
            path = f"{directory}/{bias}{unique_file}"

            if not os.path.isdir(path):
                continue

            for file in itertools.chain.from_iterable(itertools.starmap(
                    self.__get_files, os.walk(path))):
                self.changed_files[key].append(
                    file[len(directory) + 1:].replace("\\", "/")
                )

    def __str__(self):
        dif_file_ins = []
        for cat, files in self.changed_files.items():
            for file in files:
                dif_file_ins.append(f"{cat}:\t{file}")
        return '\n'.join(dif_file_ins)


if __name__ == "__main__":
    pass
