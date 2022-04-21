import os
from dir_changes import DirectoryChanges


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
            folders_prev.add(dir_path[len(self.dir_previous):])
        for dir_path, *_ in os.walk(self.dir_current):
            folders_curr.add(dir_path[len(self.dir_current):])
            
        return folders_prev, folders_curr

    def directory_difference(self) -> list[DirectoryChanges]:
        """
        Finds difference between two directories
        :return: List of differences between each of subfolders
        """
        prev_folders, curr_folders = self.__find_directory_sub_folders()
        difference = []
        
        for directory in prev_folders.intersection(curr_folders):
            difference.append(DirectoryChanges(
                f"{self.dir_previous}{directory}",
                f"{self.dir_current}{directory}"
            ))
        for directory in prev_folders.difference(curr_folders):
            difference.append(DirectoryChanges(
                dir_prev=f"{self.dir_previous}{directory}"
            ))
        for directory in curr_folders.difference(prev_folders):
            difference.append(DirectoryChanges(
                dir_current=f"{self.dir_current}{directory}"
            ))
        
        return list(filter(lambda ch: len(ch.file_changes) != 0, difference))

    # @staticmethod
    # def __get_current_directory_files(directory) -> list:
    #     for *dir_info, filenames in os.walk(directory):
    #         return filenames
    #
    # def __find_subdirectory_difference(self, subdir1, subdir2):
    #     sub_dirs_compared = filecmp.dircmp(subdir1, subdir2)
    #     dir1_files = self.__get_current_directory_files(subdir1)
    #     dir2_files = self.__get_current_directory_files(subdir2)


if __name__ == "__main__":
    pass
