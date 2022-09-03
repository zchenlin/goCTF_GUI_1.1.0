from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os
import glob
import subprocess as sp
import decimal
import matplotlib.pyplot as plt
import numpy as np
import math
import re

class MainWindow(QWidget):
    
    folder_num = 0
    folder_num_2 = 0
    ctf_directory = os.getcwd()
    mrc_list = []  


    def __init__(self,parent=None):
        super().__init__(parent)
 
        flo = QFormLayout()
        self.about = QPushButton("About")
        

        

        self.info = QPushButton("Instructions")
        self.info.clicked.connect(self.showdialog)
        
        flo.addRow(self.info,self.about)


        #Interface for particles split

        self.b4 = QPushButton('Locate particles.star Directory')
        self.b4.clicked.connect(self.open_file_2)

        self.b5 = QLineEdit()


        self.label_1 = QLabel('Step 1:')
        flo.addWidget(self.label_1)

        flo.addRow(self.b4,self.b5)


        self.b6 = QPushButton('Particles Split')
        self.b6.clicked.connect(self.click_b6)

        self.b7 = QLineEdit()
        flo.addRow(self.b6, self.b7)

        self.label_2 = QLabel('Step 2:')
        flo.addWidget(self.label_2)

        self.locate_folder = QPushButton('Locate star Folder')
        self.locate_folder.clicked.connect(self.click_locate_folder)
        self.folder_dir = QLineEdit()
        flo.addRow(self.locate_folder,self.folder_dir)

        self.locate_folder_mrc = QPushButton('Locate mrc Folder')
        self.locate_folder_mrc.clicked.connect(self.click_locate_folder_mrc)
        self.mrc_folder_dir = QLineEdit()
        flo.addRow(self.locate_folder_mrc, self.mrc_folder_dir)

        
        self.b3 = QLineEdit()

        self.e1 = QLineEdit('2.7')
        flo.addRow('Cs(mm)', self.e1)
        
        self.e2 = QComboBox()
        self.e2.addItems(['200','300'])
        flo.addRow('Voltage(kV)', self.e2)
        self.e2.currentTextChanged.connect(self.text_changed)

        self.e3 = QLineEdit('0.1')
        flo.addRow('Amplitude contrast', self.e3)

        self.e4 = QLineEdit()
        flo.addRow('Pixel size(A)', self.e4)

        self.e5 = QLineEdit('512')
        flo.addRow('FFT box size', self.e5)

        self.e6 = QLineEdit('30')
        flo.addRow('Min Res(A)', self.e6)

        self.e7 = QLineEdit('8')
        flo.addRow('Max Res', self.e7)

        self.e8 = QLineEdit('50000')
        flo.addRow('Min defcous(A)', self.e8)

        self.e9 = QLineEdit('500000')
        flo.addRow('Max defcous(A)', self.e9)

        self.e10 = QLineEdit('500')
        flo.addRow('Defcous step size(A)', self.e10)

        self.e12 = QComboBox()
        self.e12.addItems(['No','Yes'])
        flo.addRow("Particle refinement", self.e12)

        self.b2 = QPushButton('Run goCFT')
        self.b2.clicked.connect(self.click_b2)
        flo.addWidget(self.b2)

        self.plot = QPushButton('Optional: Plot and Calculate tilt degree') 
        self.plot.clicked.connect(self.click_plot)
        flo.addWidget(self.plot)

        self.label_3 = QLabel('Step 3:')
        flo.addWidget(self.label_3)

        self.locate_job_folder = QPushButton('Locate Job Folder to Merge')
        self.locate_job_folder.clicked.connect(self.click_locate_job_folder)

        self.job_folder_dir = QLineEdit()
        flo.addRow(self.locate_job_folder, self.job_folder_dir)

        self.merge = QPushButton('Merge to particles_goCTF.star')
        self.merge.clicked.connect(self.click_merge)
        flo.addRow(self.merge)

        
        self.setLayout(flo)
        self.setWindowTitle('goCTF')
        self.setFixedWidth(520)
        self.setFixedHeight(760)
        self.show()

        sys.exit(app.exec_())


    def open_file(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '','All Files (*.*)')
        if path != ('', ''):
            print(path[0])
        self.b3.setText('{}'.format(path[0].split('/')[-1]))

    def open_file_2(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '','All Files (*.*)')
        if path != ('', ''):
            self.b5.setText(path[0])
    
    def click_locate_folder(self):
        foo_dir = QFileDialog.getExistingDirectory(self, 'Select an directory')
        if foo_dir != '':
            self.folder_dir.setText(foo_dir)
            os.chdir(foo_dir)
    

    def click_locate_folder_mrc(self):
        foo_dir = QFileDialog.getExistingDirectory(self, 'Select an directory')
        if foo_dir != '':
            self.mrc_folder_dir.setText(foo_dir)
            os.chdir(foo_dir)
            #Find all the mrc files and store them to a list  
            for file in glob.glob('*.mrc'):
                self.mrc_list.append(file)
            
    
    def click_locate_job_folder(self):
        foo_dir = QFileDialog.getExistingDirectory(self, 'Select an directory')
        if foo_dir != '':
            self.job_folder_dir.setText(foo_dir)
            os.chdir(foo_dir)


    #Processing after click "goctf"
    def click_b2(self):
        os.system('chmod 777 ./goctf')
        os.chdir(self.folder_dir.text())
        #Symbolic link  mrc file to the directory of star file
        command_ln = 'ln -s ' + self.mrc_folder_dir.text() + '/' + '*.mrc ./.'
        print(command_ln)
        try:
            os.system(command_ln)
        except: 
            pass
        print('Test')
        for file in glob.glob('*.mrc'):
                print(file)
        #Get the current directory
        #current_directory = os.getcwd()
        #print(current_directory)
        with open('goCTF.sh','w') as wrapper: 
            wrapper.writelines('#!/bin/csh -f' + '\n')
            wrapper.writelines('#' + '\n')
            wrapper.writelines('set filename1 = $' + '1' + '\n')
            wrapper.writelines('set filename2 = $' + '2' + '\n')
            wrapper.writelines('../goctf << eos' + '\n')
            wrapper.writelines('$filename1' + '\n')
            wrapper.writelines('output.mrc' + '\n')
            wrapper.writelines(self.e4.text() + '\n')
            wrapper.writelines(self.e2.currentText() + '\n')
            wrapper.writelines(self.e1.text() + '\n')
            wrapper.writelines(self.e3.text() + '\n')
            wrapper.writelines(self.e5.text() + '\n')
            wrapper.writelines(self.e6.text() + '\n')
            wrapper.writelines(self.e7.text() + '\n')
            wrapper.writelines(self.e8.text() + '\n')
            wrapper.writelines(self.e9.text() + '\n')
            wrapper.writelines(self.e10.text() + '\n')
            wrapper.writelines(self.e12.currentText() + '\n')
            wrapper.writelines('eos')
        os.system('chmod 777 goCTF.sh')

        folder_name = 'job'
        
        #Track the number of folders already being created
        self.folder_num = self.folder_num + 1 
        
        #Create the folder to store the output
        indicator = True
        while indicator: 
            try:
                os.mkdir(folder_name + str(self.folder_num))
            except: 
                self.folder_num = self.folder_num + 1 
            else: 
                indicator = False
        #Direct to the new folder after it has being created
        #os.chdir(folder_name + str(self.folder_num))


        for mrc in glob.glob('*.mrc'): 
                #print(mrc)
                #mrc_directory = self.mrc_folder_dir.text() + '/' + mrc 
                #print(mrc_directory)
                command = './goCTF.sh ' + mrc + ' >> output_statistics.txt'
                print(command)
                file_go_star = mrc.replace('.mrc','_goCTF.star')
                #test command
                os.system(command)
                # add a new working director. ex. job001
           

        #Return to the parent folder and transfer the output goCTF.star files to the output folder
        #os.chdir('..')
        for mrc_2 in self.mrc_list:
            go_star = mrc_2.replace('.mrc','_goCTF.star')
            command_2 = 'mv ' + go_star + ' ' + folder_name + str(self.folder_num)
            try: 
                os.system(command_2)
            except: 
                print('No such file')
        command_mv_output = 'mv ' + 'output_statistics.txt ' + folder_name + str(self.folder_num)
        os.system(command_mv_output)
        print('Done')
        

    
    #Processing the click of "Particles Split"
    def click_b6(self):

            folder_name_2 = 'particles_split_'

            #Use to track the number of folder being created 
            self.folder_num_2 = self.folder_num_2 + 1 

            #Every time begin a new particle split, we need to return to where goctf is located
            os.chdir(self.ctf_directory)

            #Create folder which contains the split particles star files
            indicator_2 = True
            while indicator_2: 
                try:
                    os.mkdir(folder_name_2+ str(self.folder_num_2))
                except: 

                    self.folder_num_2= self.folder_num_2 + 1 
                else: 
                    indicator_2 = False
            os.chdir(folder_name_2 + str(self.folder_num_2))
            
            #The directory of particles_split.py; normally it should be in the same directory with goctf
            particles_split_dir =  self.ctf_directory + '/particles_split.py'

            #Call particles_split.py 
            output = sp.run(['python3', particles_split_dir, '-f', self.b5.text()], capture_output=True)

            #Return the output to the interface
            self.b7.setText(str(output.stdout))


    def click_merge(self):     
        merge_command = 'cat'
        for file_job_folder in glob.glob('*.star'):
            merge_command = merge_command + ' ' + file_job_folder

        merge_command =  merge_command + ' > particles_goCTF.star'
        os.system(merge_command)

    
    def click_plot(self):
        folder_name = 'job'
        plot_command = folder_name + str(self.folder_num)
        os.chdir(plot_command)
        current_directory = os.getcwd()
        print(current_directory)
        with open('output_statistics.txt') as f:
            lines = f.readlines()

            regex = 'best multi_fit: Y = .*\+ (.*) X'
            result_num = []
            for line in lines: 
                results = re.findall(regex, str(line))
                for result in results: 
                    result_num.append(round(float(result),3))
            
            n, bins, patches = plt.hist(result_num, bins=100,range=(-5,5))
            mode_index = n.argmax()
            pixel = float(self.e4.text())
            title_1 = 'The peak bin is:(' + str(bins[mode_index]) + ',' + str(bins[mode_index+1])+')' +'\n'
            title_2 = 'The tilt degree is ' + str(math.atan((bins[mode_index] + bins[mode_index+1])/2)*pixel*57.3)
            plt.title(title_1+title_2)
            plt.show()



    def text_changed(self, s):
        if s == '200': 
            self.e3.setText('0.1')
        else: 
            self.e3.setText('0.07')


    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Message box pop up window")
        msg.setDetailedText('Yes')
        msg.setStandardButtons(QMessageBox.Ok)
        #self.msgBox.buttonClicked.connect(msgButtonClick)
        msg.exec_()

      
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Win = MainWindow()
    Win.show()
    sys.exit( app.exec_() )

