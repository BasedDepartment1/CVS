import os
from cvs.file_changes import FileChanges
from cvs.init import Init
from cvs.directory_difference import DirectoryDifference, DiffKeys
import json


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
        # Todo make test of it:
        C:/Users/Jopa/Slona/main.py -> Slona/main.py
        Slona/main.py -> Slona/main.py
        Slona\\main.py -> Slona/main.py

        :param path: path to file/directory to cut
        :return: relative path to file/directory
        """

        return os.path.relpath(path).replace("\\", "/")

    @staticmethod
    def __find_file_difference(path: str) -> FileChanges:
        """
        Finds difference between the current file and the file
        from index state folder
        :param path: path to current file
        :return: changes done to a file
        """
        return FileChanges.find_difference(Init.index_folder_path, path)

    @staticmethod
    def __find_dir_difference(path: str) -> list[FileChanges, tuple]:
        """
        Finds difference between current directory and directory
        from index state folder
        :param path: path to current directory
        :return: list of FileChanges for files and tuples
        (directory_path, DiffKeys.[difference type]) for directories
        """
        res = DirectoryDifference(Init.index_folder_path, path)
        changed_files = []

        for key, staged_change in res.changed_files:
            if key == DiffKeys.MODIFIED:
                changed_files \
                    .append(Adder.__find_file_difference(staged_change))
            else:
                changed_files.append((key, staged_change))

        return changed_files

    @staticmethod
    def __serialize_difference(differences: list[FileChanges, tuple[DiffKeys,
                                                                    list]]) \
            -> None:
        """
        Add all calculated differences to .json file
        If file or directory difference exists, override it
        :param differences: differences between current and index state
        """
        def jsonify(jsoned_string, file_path):
            return file_path + jsoned_string

        path_to_json_file = Init.rep_path + "statham.json"  # путь (не путю) к json файлу
        serialized_changes = []

        # TODO унифицировать построение json-строки
        for diff in differences:
            if isinstance(diff, FileChanges):
                serialized_changes = [jsonify(inst.to_json(), diff.file_path)
                                      for inst in diff.changes]
            else:
                # если в diff Tuple'ы вида (DiffKeys.MODIFIED|DELETED|NEWFILE, [changes]), то делаем json из них
                # надо как-то унифицировать форму этого jsona, потому что выше мы строим его по-другому
                # то есть [jsonify(inst.to_json(), diff.file_path) for inst in diff.changes] хорошо бы как-то так же строить строку
                # иначе потом не разберем что где

                serialized_changes.append(json.dumps({diff[0]: diff[1]}))
        # сравниваем json старый с новым, ищем их объединение
        # если нормальные json-строки будут (одного формата), то сравнивать их можно легко, простым проходам по значениям:
        # например вот так:  json_data[i][f"{key}"], json-data получается с помощью json.load (не loads, по аналогии понятно что это даст строку)
        #TODO найти объединение json'а старого и нового, записать их в тот же (он у нас один, лежит в .cvs) json
        with open(path_to_json_file, "w") as js_file:
            old_data = json.load(js_file)
            for stage in old_data:
                if stage not in serialized_changes:
                    serialized_changes.append(stage)
            json.dump(serialized_changes, js_file, indent=4)

        # Сначала считываем то что есть в jsonе
        # Делаем объединение того что есtь и нового
        # ПЕРЕзаписываем в тот же json

        #TODO всего по add осталось: две TODOшки выше и сам def add()