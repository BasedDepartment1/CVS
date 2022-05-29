# from file_changes import FileChanges
# from differences import Differences
# import json
#
#
# # дерево коммитов в json файле с основной инфой (комментарий прошлый следующий и путь до папки с тех информацией о коммите) о каждом коммите
# # техническая информация о коммитах лежит в папке objects в виде файлов .txt
# # в .cvs хранится самая первая директория при cvs init
# # в .cvs хранится директория HEAD (последний коммит в той ветке) для ветки (папка HEADS)
# #
# # TODO to be transformed to actual folder
# # TODO implement init, creation of .cvs (hidden folder)
# # one more json : [hash] -> [path] of a commit
# class CommitInfo:
#     def __init__(self,
#                  msg: str,
#                  prev_name: str,
#                  next_name: str,
#                  path_to_obj: str):
#         self.msg = msg
#         self.prev_name = prev_name
#         self.next_name = next_name
#         self.path_to_obj = path_to_obj
#         self.differences = Differences(путь к headу (лежит в CVS), путь к текущей (содержит CVS))
#
#     def jsonify(self):
#         return {"message": self.msg,
#                 "previous": self.prev_name,
#                 "next": self.next_name,
#                 "path to obj folder": self.path_to_obj}
#
#
# def add_to_working_tree(new_commit: CommitInfo):
#     with open("tree.json", "w+", encoding="utf-8", errors='ignore') as w_tree:
#         json.dump(new_commit.jsonify(), w_tree, indent=4)
#
#
# class CommitTechInfoBuilderForObjectAndNameOfThisClassCanSurelyBeEvenLonger:
#     def __init__(self):
#
