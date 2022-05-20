# import unittest
# import os
# import shutil
# from cvs.file_changes import FileChanges
# from cvs.dir_changes import DirectoryChanges
# from cvs.data_transfer_objects import DifferenceDTO
#
#
# class DirectoryChangesTests(unittest.TestCase):
#     def setUp(self) -> None:
#         os.mkdir("first_directory")
#         os.mkdir("second_directory")
#
#         self.dir1 = os.getcwd() + "\\first_directory"
#         self.dir2 = os.getcwd() + "\\second_directory"
#
#     def tearDown(self) -> None:
#         shutil.rmtree(self.dir1)
#         shutil.rmtree(self.dir2)
#
#     def test_deleted_file(self):
#         with open(f"{self.dir1}\\testFile1.txt", "w+", encoding='utf-8',
#                   errors='ignore') as f1_1:
#             f1_1.write("Vanished")
#
#         trash = DirectoryChanges(dir_prev=self.dir1, dir_current=self.dir2)
#
#         expected = [FileChanges(f"{self.dir1}\\testFile1.txt", None)]
#
#         actual = trash.file_changes
#         for element in expected:
#             self.assertIn(element, actual)
#
#         for element in actual:
#             self.assertIn(element, expected)
#
#     def test_added_file(self):
#         with open(f"{self.dir2}\\testFile3.txt", "w+", encoding='utf-8',
#                   errors='ignore') as f2_2:
#             f2_2.write("Appeared")
#
#         trash = DirectoryChanges(dir_prev=self.dir1, dir_current=self.dir2)
#         expected = [FileChanges(None, f"{self.dir2}\\testFile3.txt")]
#         actual = trash.file_changes
#
#         for element in expected:
#             self.assertIn(element, actual)
#
#         for element in actual:
#             self.assertIn(element, expected)
#
#     def test_file_changed(self):
#         with open(f"{self.dir1}\\testFile2.txt", "w+", encoding='utf-8',
#                   errors='ignore') as f1_2, \
#                 open(f"{self.dir2}\\testFile2.txt", "w+", encoding='utf-8',
#                      errors='ignore') as f2_1:
#
#             f1_2.write("Existed")
#             f2_1.write("Exists")
#
#         trash = DirectoryChanges(dir_prev=self.dir1, dir_current=self.dir2)
#
#         expected = [
#             FileChanges(f"{self.dir1}\\testFile2.txt",
#                         f"{self.dir2}\\testFile2.txt"),
#         ]
#         actual = trash.file_changes
#
#         for element in expected:
#             self.assertIn(element, actual)
#
#         for element in actual:
#             self.assertIn(element, expected)
#
#
# if __name__ == '__main__':
#     unittest.main()
