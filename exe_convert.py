'''GUI for PyInstaller written using PyQt4'''
#importing necessary python modules
from PyQt4 import QtGui,QtCore,uic
import imageio as im
import PyInstaller
import sys
import os

#load ui path of ui window designed using QtDesigner
ui_path = "exe_window.ui"
icon_path = "convert.png"

#initialize ui
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        ui = uic.loadUi(ui_path,self)
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.textEdit.setReadOnly(True)
        #point all browse buttons to act as file browsers
        self.browsebtn.clicked.connect(lambda :self.fileBrowse(0))
        self.browsebtn_2.clicked.connect(lambda :self.fileBrowse(1))
        self.browsebtn_3.clicked.connect(lambda :self.fileBrowse(2))
        self.browsebtn_4.clicked.connect(lambda :self.fileBrowse(3))
        self.convert_btn.clicked.connect(lambda :self.convert())
        self.labelPy.setVisible(False)
        self.labelDir.setVisible(False)
        self.labelRadio.setVisible(False)
        self.labelExe.setVisible(False)


    def fileBrowse(self,choice):
        '''function to get filepaths'''
        if choice==0:
            filename = QtGui.QFileDialog.getOpenFileName(self,'Choose .py file','','*.py')
            self.pyLE.setText('')
            self.pyLE.setText(filename)
        elif choice==1:
            filename = QtGui.QFileDialog.getExistingDirectory(self,'Choose a folder')
            self.outLE.setText('')
            self.outLE.setText(filename)
        elif choice==2:
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Choose icon file', '', '*.png *.jpg *.jpeg *.png *.ico')
            self.icoLE.setText('')
            self.icoLE.setText(filename)
        elif choice==3:
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Choose python interpreter', '', '*.exe')
            self.exeLE.setText('')
            self.exeLE.setText(filename)


    def convert(self):
        '''all conversions happen here'''
        py_file = self.pyLE.text()
        if py_file=='':
            self.pyLE.setStyleSheet("""QLineEdit{border: 1px solid red};""")
            self.labelPy.setStyleSheet("""QLabel{color:red}""")
            self.labelPy.setVisible(True)
            self.labelPy.setText("Choose .py file to convert.")
        else:
            self.labelPy.setVisible(False)
            self.pyLE.setStyleSheet("""QLineEdit{border: 0.1px solid black};""")
            out_file = self.outLE.text()
            if out_file=='':
                self.outLE.setStyleSheet("""QLineEdit{border: 1px solid red};""")
                self.labelDir.setStyleSheet("""QLabel{color:red}""")
                self.labelDir.setVisible(True)
                self.labelDir.setText("Choose output folder.")
            else:
                self.labelDir.setVisible(False)
                self.outLE.setStyleSheet("""QLineEdit{border: 0.1px solid black};""")
                interpreter = self.exeLE.text()
                if interpreter=='':
                    self.exeLE.setStyleSheet("""QLineEdit{border: 1px solid red};""")
                    self.labelExe.setStyleSheet("""QLabel{color:red}""")
                    self.labelExe.setVisible(True)
                    self.labelExe.setText("Choose python interpreter.")
                else:
                    self.labelExe.setVisible(False)
                    self.exeLE.setStyleSheet("""QLineEdit{border: 0.1px solid black};""")
                    radios = [self.oneFile, self.oneDir]
                    flag = ''
                    for i in range(0, 2):
                        if radios[i].isChecked():
                            flag = radios[i].objectName()
                            if flag == 'oneFile':
                                flag = '-F'
                            elif flag == 'oneDir':
                                flag = '-D'

                    if flag=='':
                        self.labelRadio.setStyleSheet("""QLabel{color:red}""")
                        self.labelRadio.setVisible(True)
                        self.labelRadio.setText("Choose mode to package exe as.")

                    else:
                        self.labelRadio.setVisible(False)
                        icon_file = self.icoLE.text()
                        # img to .ico conversion
                        try:
                            img = im.imread(icon_file)
                            im.imwrite(os.path.dirname(icon_file) + '/icon.ico', img)
                            print("Convert with .ico")
                            os.chdir(out_file)
                            cmd = '{0} -m PyInstaller {1} -i {2} {3}'.format(interpreter, py_file, os.path.dirname(icon_file) + '/icon.ico', flag)


                        except ValueError:
                            print("Convert without .ico")
                            os.chdir(out_file)
                            print(os.getcwd())
                            # os.system(cmd_dir)
                            cmd = '{0} -m PyInstaller {1} {2}'.format(interpreter, py_file, flag)
        try:
            #perform actual exe conversion and pipe output to QTextEdit
            self.out_process = QtCore.QProcess(self)
            self.out_process.start(cmd)
            self.out_process.readyReadStandardOutput.connect(self.handleStdOut)
            self.out_process.readyReadStandardError.connect(self.handleStdErr)

        except UnboundLocalError:
            pass

    def handleStdOut(self):
        data = self.out_process.readAllStandardOutput().data()
        self.textEdit.setText(data.decode('utf-8'))

    def handleStdErr(self):
        data = self.out_process.readAllStandardError().data()
        self.textEdit.setText(data.decode('utf-8'))
        # self.textEdit.append(out_process)






Qapp = QtGui.QApplication(sys.argv)
Qwin = MainWindow()
Qwin.show()
try:
    sys.exit(Qapp.exec_())
except:
    pass