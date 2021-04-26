# HEADER
    # Developers:   Bobby Davis, Christopher Scott, Cody Todd
    
    # Course:       CST 205
    
    # Description:  Create a GUI that allows users to search for and manipulate images in a simple and easy to understand way.
    #               Users can: Enter keywords to search for images, see how many likes a photo has, save an image, apply image filters, 
    #               make a collage from save pictures, save edited images or a collage.        
# ----------------------------------------------------------------------------------------------------------------------------------------------

# IMPORTS
import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QDialog, QTextBrowser, QComboBox, QLineEdit
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap
from PIL import Image
import requests, json
from pprint import pprint

# ----------------------------------------------------------------------------------------------------------------------------------------------

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
            'per_page' : 1
        }
        endpoint = 'https://api.unsplash.com/search/collections'
        try:
            request = requests.get(endpoint, params=payload)
            data = request.json()
            pprint(data)
        except:
            print('please try again')

        if data:
            for image in data['results']:
                im = Image.open(requests.get(image['cover_photo']['urls']['full'], stream=True).raw)
                im.show()
        else:
            print('no data')

# ----------------------------------------------------------------------------------------------------------------------------------------------

# Initalize and Run application
app = QApplication(sys.argv)
main = Homepage()
main.show() # Display U.I.
sys.exit(app.exec_())
