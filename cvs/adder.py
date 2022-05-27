import os
import re
from cvs.file_changes import FileChanges


class Adder:
    @staticmethod
    def add(path: str) -> None:
        """
        Adds a file or directory to the index

        :raises FileNotFoundError if file/directory does
        not belong to repository
        :param path: path to file/directory
        """
        pass

    @staticmethod
    def __remove_dir_path(path: str) -> str:
        """
        Removes the full useless part of a path if it exists

        For example:
        We have set up repository in folder Slona:

        C:/Users/Jopa/Slona/main.py -> Slona/main.py
        Slona/main.py -> Slona/main.py

        :param path: path to file/directory to cut
        :return: relative path to file/directory
        """
        pass

    @staticmethod
    def __find_file_difference(path: str) -> FileChanges:
        """
        Finds difference between the current file and the file
        from index state folder
        :param path: path to current file
        :return: changes done to a file
        """
        pass

    @staticmethod
    def __find_dir_difference(path: str) -> list:
        """
        Finds difference between current directory and directory
        from index state folder
        :param path: path to current directory
        :return: list of FileChanges for files and tuples
        (directory_path, DiffKeys.[difference type]) for directories
        """
        pass

    @staticmethod
    def __serialize_difference(differences) -> None:
        """
        Add all calculated differences to .json file
        If file or directory difference exists, override it
        :param differences: differences between current and index state
        """
        pass
