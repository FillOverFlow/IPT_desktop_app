from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget,QFileDialog
from sys import platform
from os import path
from main import main
import sys 
import webbrowser as web
import shutil
import time
import os 
import glob

''' TODO : fix change static path => D:\True\engine\parameter
    line: 31
    line: 86
    line: 124
'''

class Setting():
    def __init__(self, csv_path='' , video_path='') -> None:
        self.csv_path = csv_path
        self.video_path = video_path
        
    def set_csv_path(self,csv_path):
        self.csv_path = csv_path
    
    def get_csv_path(self) -> str:
        return self.csv_path
        
class WelcomeScreen(QDialog):
    def __init__(self) -> None:
        super().__init__()
        loadUi('screens/welcomescreen.ui',self)
        is_have_weight = True if len(os.listdir('D:\True\engine\parameter')) > 1 else False
        if is_have_weight:
            self.upload_weight.clicked.connect(self.goto_justonefile)
        else:
            self.upload_weight.clicked.connect(self.goto_uploadweight)
        
    def goto_uploadweight(self):
        upload_weight = UploadWeightScreen()
        widget.addWidget(upload_weight)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def goto_justonefile(self):
        justone_file = JustOneFileScreen()
        widget.addWidget(justone_file)
        widget.setCurrentIndex(widget.currentIndex()+1)

class JustOneFileScreen(QDialog):
    def __init__(self) -> None:
        super().__init__()
        loadUi('screens/justonefile_screen.ui',self)
        self.progressBar.setVisible(False)
        self.preview_btn.setVisible(False)
        self.choose_file_btn.clicked.connect(self.choose_file_action)
        self.preview_btn.clicked.connect(self.preview_one_web)
        self.process_btn.clicked.connect(self.goto_justonefile)
        self.setting_btn.clicked.connect(self.goto_uploadweight)
        
    def goto_uploadweight(self):
        upload_weight = UploadWeightScreen()
        widget.addWidget(upload_weight)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def goto_justonefile(self):
        justone_file = JustOneFileScreen()
        widget.addWidget(justone_file)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def choose_file_action(self):
        path = QFileDialog.getOpenFileName(self,'Open a file','','All Files (*.*)')
        
        if path != ('', ''):
            print("File path :", path[0])
        
        self.action_process_video(path[0])
    
    def preview_one_web(self):
        print("open web browser..")
        web.open('https://dev.sintanan.indezy.tech')
    
    def action_process_video(self,path):
        print("process video :", path)
        self.choose_file_btn.setVisible(False)
        self.progressBar.setVisible(True)
        video_path = path
        weight_path = r"D:\True\engine\parameter"
                
        print("[*] process main:")
        print("[+] video_path :", video_path)
        print("[+] weight_path:",weight_path)
        main(video_path,weight_path)
    
        self.progressBar.setValue(100)
        self.progressBar.setVisible(False)
        self.preview_btn.setVisible(True)
        

class UploadWeightScreen(QDialog):
    def __init__(self) -> None:
        super().__init__()
        loadUi('screens/upload_weight.ui',self)
        self.choose_file_btn.clicked.connect(self.choose_file_action)
        self.process_btn.clicked.connect(self.goto_justonefile)
        self.setting_btn.clicked.connect(self.goto_uploadweight)
        
    def goto_uploadweight(self):
        upload_weight = UploadWeightScreen()
        widget.addWidget(upload_weight)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def goto_justonefile(self):
        justone_file = JustOneFileScreen()
        widget.addWidget(justone_file)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def choose_file_action(self):
        print("Choose file ...")
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        
        if path != ('', ''):
            print("File path : ", path)
        
        src_files = os.listdir(path)
        dest = r'D:\True\engine\parameter'
        
         #delete old weight
        dir = r'D:\True\engine\parameter'
        filelist = glob.glob(os.path.join(dir, "*"))
        for f in filelist:
            print("remove =>",f)
            os.remove(f)
        
        for file_name in src_files:
            full_file_name = os.path.join(path, file_name)
            if os.path.isfile(full_file_name):
               
                shutil.copy(full_file_name, dest)
        print("[+] copy all file success ")
        setting.set_csv_path(dest)
        print("[+] set weight path :",setting.get_csv_path())
    
    

#main

setting = Setting()
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(561)
widget.setFixedWidth(931)
widget.show()


app.exec()

# if __name__ == "__main__":
#     video_path = r"D:\True\Clycle-time-monitoring-True-Project\Normal.avi"
    
#     print("[*] process main:")
#     print("[+] video_path :", video_path)
#     print("[+] weight_path:",weight_path)
#     main(video_path,weight_path)

# try:
#     sys.exit(app_exec())
# except:
#     print("Exiting")