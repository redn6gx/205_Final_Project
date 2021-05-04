import sys
from PySide6.QtWidgets import QListWidgetItem,QMainWindow, QGridLayout, QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QDialog, QTextBrowser, QComboBox, QLineEdit, QTabWidget, QListWidget, QListView
from PySide6.QtCore import Qt, Slot, QSize, Signal
from PySide6.QtGui import QPixmap, QIcon
from PIL import Image
import requests, json
from pprint import pprint
import os, pickle

class clickableImage(QLabel):
    clicked = Signal(str)

    def __init__(self,image,data):
        super(clickableImage,self).__init__()
        pixmap = QPixmap()
        print('load (%s) %r' % (pixmap.load(image), image))
        self.data = data
        self.setPixmap(image)

    def mousePressEvent(self,event):
        self.clicked.emit(self.objectName())

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.tabs = QTabWidget(self)
        # self.tabs.setTabsClosable(True)
        layout = QGridLayout(self)
        layout.addWidget(self.tabs, 0, 0, 1, 2)
        self.tab1 = Homepage()
        self.tabs.addTab(self.tab1,"Home")

    def createNewTab(self,imgs):
        
        
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == 'Results':
                self.tabs.removeTab(i)
        viewer = QListWidget(self)
        viewer.setViewMode(QListView.IconMode)
        viewer.setIconSize(QSize(256, 256))
        viewer.setResizeMode(QListView.Adjust)
        viewer.setSpacing(10)
        # self.mybtn = QPushButton("close tab")
        # btn = QListWidgetItem()
        # wid = QWidget()
        # widlay = QHBoxLayout()
        # widlay.addWidget(self.mybtn)
        # wid.setLayout(widlay)
        # btn.setSizeHint(wid.sizeHint())

        # viewer.addItem(btn)
        # viewer.setItemWidget(btn,wid)

        folder = './results'
        for filename in os.listdir(folder):
            path = folder +"/"+ filename
            with open(path,'rb') as thefile:
                imag = pickle.load(thefile)
            im = Image.open(requests.get(imag['cover_photo']['urls']['thumb'], stream=True).raw)
            im.save(path+".jpg")
            pixmap = QPixmap()
            ipath = path + ".jpg"
            print('load (%s) %r' % (pixmap.load(ipath), ipath))
            item = QListWidgetItem(ipath)
            item.setIcon(QIcon(ipath))
            viewer.addItem(item)
            try:
                if os.path.isfile(ipath) or os.path.islink(ipath):
                    os.unlink(ipath)
                elif os.path.isdir(ipath):
                    shutil.rmtree(ipath)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        index = self.tabs.count()
        self.tabs.addTab(viewer, 'Results')
        self.tabs.setCurrentIndex(index)

class Homepage(QWidget):
    def __init__(self):
        super().__init__()


        # Declare Widgets
        self.homepage_label = QLabel('Home')
        self.search_label = QLabel('Find an Image!')
        self.srch_box = QLineEdit() # input field for search
        self.srch_btn = QPushButton("Search")

        # Create U.I. Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.homepage_label)
        vbox.addWidget(self.search_label)
        vbox.addWidget(self.srch_box)
        vbox.addWidget(self.srch_btn)
        self.setLayout(vbox) # apply layout to this class

         # Listeners
        self.srch_btn.clicked.connect(self.find_images)

    @Slot()
    def find_images(self):
        print("Finding Match...")

        # Connect to Unsplash API
        api_key = 'uAJtv5-qrHmTRbHc-7xqzv44tPPPZ2tOL39g3kP3lvM'

        payload = {
            'client_id': api_key,
            'query' : self.srch_box.text(),
            'page' : 1,
            'per_page' : 5
        }
        endpoint = 'https://api.unsplash.com/search/collections'
        try:
            request = requests.get(endpoint, params=payload)
            data = request.json()
            #pprint(data)
        except:
            print('please try again')

        if data:
            i = 1
            imgs = []
            for image in data['results']:
                im = Image.open(requests.get(image['cover_photo']['urls']['full'], stream=True).raw)
                imgs.append(image)
                with open("./results/result"+str(i),"wb") as myfile:
                    pickle.dump(image, myfile)
                name = "./results/result"+str(i)+".jpg"
                #im.save(name)
                with open("./results/result"+str(i),"rb") as my_file:
                    unpick = pickle.load(my_file)
                #pprint(unpick)
                i += 1


            #Deleting images after use
            # folder = './results'
            # for filename in os.listdir(folder):
            #     file_path = os.path.join(folder, filename)
            #     try:
            #         if os.path.isfile(file_path) or os.path.islink(file_path):
            #             os.unlink(file_path)
            #         elif os.path.isdir(file_path):
            #             shutil.rmtree(file_path)
            #     except Exception as e:
            #         print('Failed to delete %s. Reason: %s' % (file_path, e))
            window.createNewTab(imgs)
        else:
            print('no data')    

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(800, 150, 650, 500)
    window.show()
    sys.exit(app.exec_())