# HEADER
    # Developers:   Bobby Davis, Christopher Scott, Cody Todd
    
    # Course:       CST 205
    
    # Description:  Create a GUI that allows users to search for and manipulate images in a simple and easy to understand way.
    #               Users can: Enter keywords to search for images, see how many likes a photo has, save an image, apply image filters, 
    #               make a collage from save pictures, save edited images or a collage.        
# ----------------------------------------------------------------------------------------------------------------------------------------------

# IMPORTS
import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QDialog, QTextBrowser, QComboBox, QLineEdit, QTabWidget
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap
from PIL import Image
import requests, json
from pprint import pprint
import os

# Global variables

# ----------------------------------------------------------------------------------------------------------------------------------------------
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'CST205 Final'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = MyTableWidget()
        self.setCentralWidget(self.table_widget)
        
        self.show()
        
class MyTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = Homepage()
        self.tab2 = results("test")
        self.tabs.resize(300,200)

        self.tabs.addTab(self.tab1,"Homepage")
        self.tabs.addTab(self.tab2,"Results")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

class results(QWidget):
    def __init__(self,name):
        super().__init__()

        # Declare Widgets
        self.im = None
        self.label = QLabel('Results')
        pixmap = QPixmap(name)
        pixmap = pixmap.scaled(500,500,Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)

        

        # Create U.I. Layout
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.setLayout(self.vbox) # apply layout to this class




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
        

    
    def createNewTab(self):
        viewer = QListWidget(self)
        viewer.setViewMode(QListView.IconMode)
        viewer.setIconSize(QSize(256, 256))
        viewer.setResizeMode(QListView.Adjust)
        viewer.setSpacing(10)

        self.mybtn = QPushButton("close tab")
        btn = QListWidgetItem()
        wid = QWidget()
        widlay = QHBoxLayout()
        widlay.addWidget(self.mybtn)
        wid.setLayout(widlay)
        btn.setSizeHint(wid.sizeHint())

        viewer.addItem(btn)
        viewer.setItemWidget(btn,wid)

        name = self.edit.text()
        folder = './results'
        for filename in os.listdir(folder):
            path = folder +"/"+ filename
            pixmap = QPixmap()
            print('load (%s) %r' % (pixmap.load(path), path))
            item = QListWidgetItem(os.path.basename(path))
            item.setIcon(QIcon(path))
            viewer.addItem(item)
        index = self.tabs.count()
        self.tabs.addTab(viewer, 'Tab%d' % (index + 1))
        self.tabs.setCurrentIndex(index)

    # Function to find multiple images by keyword(s)
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
            pprint(data)
        except:
            print('please try again')

        if data:
            i = 1
            imgs = []
            for image in data['results']:
                im = Image.open(requests.get(image['cover_photo']['urls']['full'], stream=True).raw)
                imgs.append(im)
                name = "./results/result"+str(i)+".jpg"
                im.save(name)
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
            self.createNewTab
        else:
            print('no data')
    



# ----------------------------------------------------------------------------------------------------------------------------------------------

# Initalize and Run application
app = QApplication(sys.argv)
main = App()
main.show() # Display U.I.
sys.exit(app.exec_())
