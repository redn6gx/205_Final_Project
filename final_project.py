# HEADER
    # Developers:   Bobby Davis, Christopher Scott, Cody Todd
    
    # Course:       CST 205
    
    # Description:  Create a GUI that allows users to search for and manipulate images in a simple and easy to understand way.
    #               Users can: Enter keywords to search for images, see how many likes a photo has, save an image, apply image filters, 
    #               make a collage from save pictures, save edited images or a collage.        
# ----------------------------------------------------------------------------------------------------------------------------------------------

# IMPORTS
import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QDialog, QTextBrowser, QComboBox, QLineEdit, QGroupBox
from PySide6.QtCore import Qt, Slot, QEvent
from PySide6.QtGui import QPixmap
from PIL import Image
from PIL.ImageQt import ImageQt
import requests, json
from pprint import pprint

# ----------------------------------------------------------------------------------------------------------------------------------------------

# Connect to Unsplash API
api_key = 'uAJtv5-qrHmTRbHc-7xqzv44tPPPZ2tOL39g3kP3lvM'

class Homepage(QWidget):
    def __init__(self):
        super().__init__()

        # Declare Widgets
        self.homepage_label = QLabel('Home')
        self.search_label = QLabel('Find an Image!')
        self.srch_box = QLineEdit() # input field for search
        self.srch_btn = QPushButton("Search")

        # Create U.I. Layout
        mbox = QVBoxLayout()

        vbox = QVBoxLayout()
        vbox.addWidget(self.homepage_label)
        vbox.addWidget(self.search_label)
        vbox.addWidget(self.srch_box)
        vbox.addWidget(self.srch_btn)

        gbox1 = QGroupBox()
        gbox1.setLayout(vbox)
        mbox.addWidget(gbox1)

        # Homes Images Layout
        images = []
        images = self.getHomepageImages()

        # Create layout for images
        vbox2 = QHBoxLayout()

        i = 0
        for img in images:
            self.label = QLabel()
            # pic = Image.open(requests.get(img['urls']['thumb'], stream=True).raw)

            pixmap1 = QPixmap(img)

            pixmap1 = pixmap1.scaled(300, 300, Qt.KeepAspectRatio)

            self.label.setPixmap(pixmap1)

            temp_vbox = QVBoxLayout()
            temp_vbox.addWidget(self.label)  

            gbox2 = QGroupBox()
            gbox2.setLayout(temp_vbox)
            gbox2.setStyleSheet("background-color: grey")
            
            vbox2.addWidget(gbox2)
            i += 1

        gbox3 = QGroupBox()
        gbox3.setLayout(vbox2)
        mbox.addWidget(gbox3)
        self.setLayout(mbox)

        # Styling
        self.setStyleSheet("""
            color: orange;
            font-family: Comfortaa;
            """)
        self.srch_btn.setStyleSheet(":hover { background-color:cyan }")
        gbox1.setStyleSheet("""
            font-size: 18px
            """)

         # Listeners
        self.srch_btn.clicked.connect(self.find_images)

    # Function to find multiple images by keyword(s)
    @Slot()
    def find_images(self):
        print("Finding Match...")

        payload = {
            'client_id': api_key,
            'query' : self.srch_box.text(),
            'page' : 1,
            'per_page' : 1
        }
        endpoint = 'https://api.unsplash.com/search/photos'
        try:
            request = requests.get(endpoint, params=payload)
            data = request.json()
            pprint(data)
        except:
            print('please try again')

        if data:
            for image in data['results']:
                im = Image.open(requests.get(image['urls']['thumb'], stream=True).raw)
                im.show()
        else:
            print('no data')

    def getHomepageImages(self):
        home_images = []
        print("Finding Match...")

        payload = {
            'client_id': api_key,
            'count' : 3
        }
        endpoint = 'https://api.unsplash.com/photos/random'
        try:
            request = requests.get(endpoint, params=payload)
            data = request.json()
            pprint(data)
        except:
            print('please try again')

        i = 1
        if data:
            for image in data:
                im = Image.open(requests.get(image['urls']['thumb'], stream=True).raw)

                loc = image['links']['html']
                print(loc)

                im_name = "image" + str(i) + ".jpg"
                im_path = "home_images/" + im_name
                im.save(im_path)
                home_images.append(im_path)
                i += 1
            return home_images
        else:
            print('no data')

# ----------------------------------------------------------------------------------------------------------------------------------------------

# Initalize and Run application
app = QApplication(sys.argv)
main = Homepage()
main.show() # Display U.I.
sys.exit(app.exec_())
