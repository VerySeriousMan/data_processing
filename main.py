# Creator: ZhangYueTao
# Version: V1.3
# Last Renew: 2024-02-28

import shutil
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
import qt_material
from data_processing import *

print(sys.setrecursionlimit(2000))


class MyClass(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyClass, self).__init__(parent)
        self.test_id = None
        self.train_id = None
        self.setupUi(self)
        self.setWindowTitle("数据预处理软件V1.3")
        self.setWindowIcon(QtGui.QIcon("sunny.ico"))
        self.dir_path = None
        self.small_dir_path = None
        self.open_dir_button.clicked.connect(self.open_dir)
        self.classify_button.clicked.connect(self.classify)
        self.change_id_button.clicked.connect(self.change_id)
        self.change_setting_button.clicked.connect(self.change_setting)
        self.open_small_dir_button.clicked.connect(self.open_small_dir)
        self.creat_txt_button.clicked.connect(self.creat_txt)

    def open_dir(self):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self)
        if os.path.isdir(dir_path):
            self.dir_path = dir_path
            self.file_path_lable.clear()
            self.file_path_lable.setText(dir_path)
            self.file_path_lable.show()
            self.pre_train_id()
            self.pre_test_id()

    def open_small_dir(self):
        small_dir_path = QtWidgets.QFileDialog.getExistingDirectory(self)
        if os.path.isdir(small_dir_path):
            self.small_dir_path = small_dir_path
            self.file_small_path_lable.clear()
            self.file_small_path_lable.setText(small_dir_path)
            self.file_small_path_lable.show()

    def pre_train_id(self):
        root_path = os.getcwd()
        file_path = os.path.join(root_path, 'trainID.txt')
        txtID = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                txtID.append(line.replace("\n", ""))
        self.train_id = txtID

    def pre_test_id(self):
        root_path = os.getcwd()
        file_path = os.path.join(root_path, 'testID.txt')
        txtID = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                txtID.append(line.replace("\n", ""))
        self.test_id = txtID

    def getid(self, filename):
        name = str(filename)
        fline = 0
        bline = 0
        if not (self.front_line.text() is None or self.front_line.text() == ''):
            fline = int(self.front_line.text())
        if not (self.back_line.text() is None or self.back_line.text() == ''):
            bline = int(self.back_line.text())

        if bline == '' or bline == 0:
            need_name = name[fline:]
        else:
            need_name = name[fline:-bline]
        return need_name

    def classify(self):
        rootpath = self.dir_path
        test_id = self.test_id
        train_id = self.train_id
        if rootpath is not None and rootpath != '':
            use_path = '/'.join(rootpath.split('/')[:-1])
            rootname = rootpath.split('/')[-1]
            for filename in os.listdir(rootpath):
                filepath = os.path.join(rootpath, filename)
                fileid = self.getid(filename)
                newpath1 = os.path.join(use_path, rootname + '_test', filename)
                newpath2 = os.path.join(use_path, rootname + '_train', filename)
                if fileid in test_id:
                    shutil.move(filepath, newpath1)
                elif fileid in train_id:
                    shutil.move(filepath, newpath2)
            self.classify_lable.setText('分类完成')
            self.classify_lable.show()

    def change_id(self):
        if self.dir_path is not None and self.dir_path != '':
            old_id = self.old_id_line.text()
            new_id = self.new_id_line.text()
            rootpath = self.dir_path
            cnt = 0

            def rename_files(directory):
                for dirpath, _, filenames in os.walk(directory):
                    for filename in filenames:
                        new_filename = filename.replace(old_id, new_id)
                        os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))

            def move_folder_contents(source_path, destination_path):
                try:
                    # Create the destination folder if it doesn't exist
                    if not os.path.exists(destination_path):
                        os.makedirs(destination_path)

                    # Recursively copy the contents of the source folder to the destination
                    for root, dirs, files in os.walk(source_path):
                        for dir_name in dirs:
                            source_dir = os.path.join(root, dir_name)
                            destination_dir = os.path.join(destination_path, os.path.relpath(source_dir, source_path))
                            if not os.path.exists(destination_dir):
                                os.makedirs(destination_dir)

                        for file_name in files:
                            source_file = os.path.join(root, file_name)
                            destination_file = os.path.join(destination_path, os.path.relpath(source_file, source_path))
                            shutil.copy2(source_file, destination_file)

                    # Remove the source folder and its contents
                    shutil.rmtree(source_path)

                    print(f"Move successful: '{source_path}' contents moved to '{destination_path}'")
                except Exception as e:
                    print(f"Error moving folder contents: {e}")

            for filename in os.listdir(rootpath):
                if old_id in filename:
                    cnt = 1
                    new_filename = filename.replace(old_id, new_id)
                    new_path = os.path.join(rootpath, new_filename)
                    old_path = os.path.join(rootpath, filename)

                    if os.path.exists(new_path):
                        move_folder_contents(old_path, new_path)
                        rename_files(new_path)
                    else:
                        os.rename(os.path.join(rootpath, filename), new_path)
                        rename_files(new_path)

            self.change_lable.clear()
            if cnt == 1:
                self.change_lable.setText('修改完成')
            else:
                self.change_lable.setText('原ID不存在')
            self.change_lable.show()

    def change_setting(self):
        if self.small_dir_path is not None and self.small_dir_path != '':
            old_set = self.old_setting_line.text()
            new_set = self.new_setting_line.text()
            rootpath = self.small_dir_path
            for dirpath, _, filenames in os.walk(rootpath):
                for filename in filenames:
                    new_filename = filename.replace(old_set, new_set)
                    os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, new_filename))
            self.change_setting_lable.setText('修改完成')
            self.change_setting_lable.show()

    def creat_txt(self):
        if self.dir_path is not None and self.dir_path != '':
            rootpath = self.dir_path
            use_path = '/'.join(rootpath.split('/')[:-1])
            rootname = rootpath.split('/')[-1]
            txt_path = os.path.join(use_path, rootname + '.txt')

            count = 1
            while os.path.exists(txt_path):
                base, extension = os.path.splitext(rootname)
                rootname = f"{base}_{count}{extension}"
                txt_path = os.path.join(use_path, rootname + '.txt')
                count += 1

            image_paths = []
            for root, dirs, files in os.walk(rootpath):
                files = [os.path.join(root, x) for x in files]
                image_paths.extend(files)
            txt = open(txt_path, mode='a', encoding='utf-8')
            for i in range(len(image_paths)):
                need_path = image_paths[i].replace('\\', '/')
                txt.writelines([need_path, '\n'])
            txt.close()
            self.txt_lable.setText('已生成txt路径')
            self.txt_lable.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyClass()
    qt_material.apply_stylesheet(app, theme='default')
    myWin.show()
    sys.exit(app.exec_())
