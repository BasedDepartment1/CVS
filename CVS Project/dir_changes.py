import filecmp
import os
from file_changes import FileChanges


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
    
    def __eq__(self, other: "DirectoryChanges"):
        return self.__prev == other.__prev \
               and self.__current == other.__current \
               and self.file_changes == other.file_changes
    
    def __repr__(self):
        return f"DirectoryChanges({self.__prev}, {self.__current}):\n" \
               f"{[repr(e) for e in self.file_changes]}"
        

if __name__ == "__main__":
    pass
