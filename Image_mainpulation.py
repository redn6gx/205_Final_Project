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
from PIL import Image, ImageDraw
import requests, json
from pprint import pprint

# ----------------------------------------------------------------------------------------------------------------------------------------------

class ImageManipulation(QWidget):
    def __init__(self):
        super().__init__()

        # Declare Widgets
        self.edit_label = QLabel('Change your image')

        # set up list and combo box option
        self.my_list = ["Pick a value", "Luminosity", "Contrast", "Colorize", "Sepia", "Negative", "Grayscale", "None"]
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

        # set up im_edit as which filter the user chose
        im_edit = self.my_combo_box.currentText()

        ##TODO change to correct image
        input_image = Image.open("image.png")
        input_pixels = input_image.load()

        output_image = Image.new("RGB", input_image.size)
        draw = ImageDraw.Draw(output_image)

        # Options are: ["Pick a value", "Luminosity", "Contrast", "Colorize", "Sepia", "Negative", "Grayscale", "None"]
        if (im_edit == "Luminosity"):
            luminosity = 80

            # Generate image
            for x in range(output_image.width):
                for y in range(output_image.height):
                    r, g, b, a = input_pixels[x, y]
                    r = int(r + luminosity)
                    g = int(g + luminosity)
                    b = int(b + luminosity)
                    draw.point((x, y), (r, g, b))

            #output_image.save("output.png")
            output_image.show()

        elif (im_edit == "Contrast"):
            # Find minimum and maximum luminosity
            imin = 255
            imax = 0
            for x in range(input_image.width):
                for y in range(input_image.height):
                    r, g, b, a = input_pixels[x, y]
                    i = (r + g + b) / 3
                    imin = min(imin, i)
                    imax = max(imax, i)

            # Generate image
            for x in range(output_image.width):
                for y in range(output_image.height):
                    r, g, b, a = input_pixels[x, y]
                    # Current luminosity
                    i = (r + g + b) / 3
                    # New luminosity
                    ip = 255 * (i - imin) / (imax - imin)
                    r = int(r * ip / i)
                    g = int(g * ip / i)
                    b = int(b * ip / i)
                    draw.point((x, y), (r, g, b))

            output_image.show()
        elif (im_edit == "Colorize"):
            # Square distance between 2 colors
            def distance2(color1, color2):
                r1, g1, b1 = color1
                r2, g2, b2, a2 = color2
                return (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2

            color_to_change = (0, 0, 255)
            threshold = 220

            # Generate image
            for x in range(output_image.width):
                for y in range(output_image.height):
                    r, g, b, a = input_pixels[x, y]
                    if distance2(color_to_change, input_pixels[x, y]) < threshold ** 2:
                        r = int(r * .5)
                        g = int(g * 1.25)
                        b = int(b * .5)
                    draw.point((x, y), (r, g, b))

            #output_image.save("output.png")
            output_image.show()
        elif (im_edit == "Sepia"):
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
            sepia_list = map(sepia, input_image.getdata())
            output_image.putdata(list(sepia_list))
            #output_image.save("output.png")
            output_image.show()
        elif (im_edit == "Negative"):
            negative_list = [(255-p[0], 255-p[1], 255-p[2])
                                for p in input_image.getdata()]
            output_image.putdata(negative_list)
            #output_image.save("output.png")
            output_image.show()
        elif (im_edit == "Grayscale"):
            new_list = [ ( (a[0]+a[1]+a[2])//3, ) * 3
                                for a in input_image.getdata() ]
            output_image.putdata(new_list)
            #output_image.save("output.png")
            output_image.show()
        else: #"Pick a value" or "None"
            input_image.show()


    @Slot()
    def on_back(self):
        print("back")
# ----------------------------------------------------------------------------------------------------------------------------------------------

# Initalize and Run application
app = QApplication(sys.argv)
main = ImageManipulation()
main.show() # Display U.I.
sys.exit(app.exec_())
