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

class ImageManipulation(QWidget):
    def __init__(self):
        super().__init__()

        # Declare Widgets
        self.edit_label = QLabel('Change your image')

        # set up list and combo box option
        self.my_list = ["Pick a value", "Sepia", "Negative", "Grayscale", "Thumbnail", "None"]
        self.my_combo_box = QComboBox()
        self.my_combo_box.addItems(self.my_list)

        self.edit_btn = QPushButton("Edit")
        self.cancel_btn = QPushButton("Back")

        # Create U.I. Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.edit_label)
        vbox.addWidget(self.my_combo_box)
        vbox.addWidget(self.edit_btn)
        vbox.addWidget(self.cancel_btn)
        self.setLayout(vbox) # apply layout to this class

        # when button is clicked send lineedit and combo box info to on_submit
        self.edit_btn.clicked.connect(self.on_edit)
        self.cancel_btn.clicked.connect(self.on_back)

    @Slot()
    def on_edit(self):
        # take image that was clicked
        # use your_search as text from the lineedit and make sure it's lowercase
        # your_search = self.my_lineedit.text()
        # your_search = your_search.lower()
        # get_count_from_search(new_dict, your_search)

        # # finds the max occurance and stores it as the max_val
        # max_list = []
        # max_val = 0
        # for key, value in new_dict.items():
        #     for counter, term in enumerate(value):
        #         if counter == 0:
        #             if term >= max_val:
        #                 if term > max_val and len(max_list) > 0:
        #                     del max_list[:len(max_list)]
        #                 max_val = term
        #                 if max_val > 0:
        #                     max_list.append((value[1], key))

        # max_list.sort()

        # set up im_edit as which filter the user chose
        im_edit = self.my_combo_box.currentText()

        im = Image.open(f'hw3_images/{max_list[0][1]}.jpg')
        # Options are: ["Pick a value", "Sepia", "Negative", "Grayscale", "Thumbnail", "None"]
        if (im_edit == "Sepia"):
            def sepia(pixel):
                if pixel[0] < 63:
                    r,g,b = int(pixel[0]*1.1), pixel[1], int(pixel[2]*.9)
                elif pixel[0]>62 and pixel[0]<192:
                    r,g,b = int(pixel[0]*1.15), pixel[1], int(pixel[2]*.85)
                else:
                    r = int(pixel[0]*1.08)
                    if r>255: r=255
                    g,b = pixel[1], pixel[2]//2  
                return r,g,b
            sepia_list = map(sepia, im.getdata())
            im.putdata(list(sepia_list))
            im.show()
        elif (im_edit == "Negative"):
            negative_list = [(255-p[0], 255-p[1], 255-p[2])
                                for p in im.getdata()]
            im.putdata(negative_list)
            im.show()
        elif (im_edit == "Grayscale"):
            new_list = [ ( (a[0]+a[1]+a[2])//3, ) * 3
                                for a in im.getdata() ]
            im.putdata(new_list)
            im.show()
        elif (im_edit == "Thumbnail"):
            def shrinker(your_image, shrink_factor):
                src = Image.open(your_image)
                w,h = src.width, src.height
                trg = Image.new('RGB', ((w//shrink_factor)+1,(h//shrink_factor)+1))
                for trg_x, src_x in enumerate(range(0, w, shrink_factor)):
                    for trg_y, src_y in enumerate(range(0, h, shrink_factor)):
                        px = src.getpixel((src_x, src_y))
                        trg.putpixel((trg_x, trg_y), px)
                trg.show()

            shrinker(f'hw3_images/{max_list[0][1]}.jpg', 2)
        else: #"Pick a value" or "None"
            im.show()


    @Slot()
    def on_back(self):
        print("back")
# ----------------------------------------------------------------------------------------------------------------------------------------------

# Initalize and Run application
app = QApplication(sys.argv)
main = ImageManipulation()
main.show() # Display U.I.
sys.exit(app.exec_())
