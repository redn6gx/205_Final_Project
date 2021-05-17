#CST 205 Image Search and Edit Engine
#A window to be able to search save and edit images
#Bobby Davis Christopher Scott and Cody Todd

import sys
from PySide6.QtWidgets import QGroupBox, QListWidgetItem,QMainWindow, QGridLayout, QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QDialog, QTextBrowser, QComboBox, QLineEdit, QTabWidget, QListWidget, QListView
from PySide6.QtCore import Qt, Slot, QSize, Signal, QObject
from PySide6.QtGui import QPixmap, QIcon
from PIL import Image, ImageDraw
import requests, json
from pprint import pprint
import os, pickle
import tempfile

api_key = 'uAJtv5-qrHmTRbHc-7xqzv44tPPPZ2tOL39g3kP3lvM'
#savedpage by Christopher Scott
class savedpage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        i = 0
        self.names = []
        self.ebutons = []
        self.dbutons = []
        folder = './saved'
        #-------------Loading saved images from ./saved------------
        if(len(os.listdir(folder)) == 0):
            #print oput nothing saved
            self.label = QLabel("Nothing Saved")
            self.layout.addWidget(self.label)
        else:
            for filename in os.listdir(folder):
                self.names.append(filename)
                self.ebutons.append(i)
                self.dbutons.append(i)
                lay = QVBoxLayout()
                gbox = QGroupBox('Result'+str(i+1))
                path = folder +"/"+ filename 
                with open(path,'rb') as thefile:
                    imag = pickle.load(thefile)
                path += ".jpg"
                im = Image.open(requests.get(imag['urls']['thumb'], stream=True).raw)
                im.save(path)
                self.ebutons[i] = QPushButton("Edit")
                self.ebutons[i].clicked.connect(lambda state=i, a=i:self.editme(state))
                self.dbutons[i] = QPushButton("Delete")
                self.dbutons[i].clicked.connect(lambda state=i, a=i: self.deleteme(state))
                pixmap = QPixmap(path)
                self.image = QLabel()
                self.image.setPixmap(pixmap)
                lay.addWidget(self.image)
                buts = QHBoxLayout()
                buts.addWidget(self.ebutons[i])
                buts.addWidget(self.dbutons[i])
                lay.addLayout(buts)
                gbox.setLayout(lay)
                self.layout.addWidget(gbox)
                try:
                    if os.path.isfile(path) or os.path.islink(path):
                        os.unlink(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
                i+=1
        print("done")
        self.setLayout(self.layout)
    @Slot()
    def editme(self,button):
        print("editing "+self.names[button])
        folder = './saved'
        
        for filename in os.listdir(folder):
            if filename == self.names[button]:
                with open("./results/result"+str(button),"rb") as my_file:
                    unpick = pickle.load(my_file)
                window.paintTab(unpick)
    @Slot()
    def deleteme(self,button):
        print("going to removing "+self.names[button])
        folder = './saved'
        for filename in os.listdir(folder):
            if filename == self.names[button]:
                print("removing "+self.names[button])
                path = folder + "/" + filename
                try:
                    if os.path.isfile(path) or os.path.islink(path):
                        os.unlink(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
                    print("removed")
                    window.savedtab()
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
                
                        


#resultpage by Christopher Scott
class resultpage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        i = 0
        self.names = []
        self.ebutons = []
        folder = './results'
        #------------loading result images from api call into result page----------
        if(len(os.listdir(folder)) == 0):
            #print oput nothing saved
            self.label = QLabel("No matching result")
            self.layout.addWidget(self.label)
        else:
            for filename in os.listdir(folder):
                self.names.append(filename)
                self.ebutons.append(i)
                lay = QVBoxLayout()
                gbox = QGroupBox('Result'+str(i+1))
                path = folder +"/"+ filename 
                with open(path,'rb') as thefile:
                    imag = pickle.load(thefile)
                path += ".jpg"
                im = Image.open(requests.get(imag['urls']['thumb'], stream=True).raw)
                im.save(path)
                self.ebutons[i] = QPushButton("Save result"+str(i+1))
                self.ebutons[i].clicked.connect(lambda state=i, a=i:self.saveme(state))
                self.ebutons[i].setStyleSheet("background-color: lightGray")
                pixmap = QPixmap(path)
                self.image = QLabel()
                self.image.setPixmap(pixmap)
                lay.addWidget(self.image)
                lay.addWidget(self.ebutons[i])
                gbox.setLayout(lay)
                gbox.setStyleSheet("background-color: grey")
                self.layout.addWidget(gbox)
                try:
                    if os.path.isfile(path) or os.path.islink(path):
                        os.unlink(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
                i+=1
        print("done")
        self.setLayout(self.layout)
    
    @Slot()
    def saveme(self,button):
        print("saving "+self.names[button])
        folder = './results'
        #----when saving finds the file and checks if already saved if not pickles the data into saved folder with generated name----
        for filename in os.listdir(folder):
            if filename == self.names[button]:
                with open("./results/result"+str(button),"rb") as my_file:
                    unpick = pickle.load(my_file)
                i =0
                sfolder = './saved'
                for files in os.listdir(sfolder):
                    with open(sfolder+"/"+files,"rb") as my_file:
                        compare = pickle.load(my_file)
                    if unpick == compare:
                        print("already saved")
                        return
                    i += 1
                tf = tempfile.NamedTemporaryFile()
                print(tf.name)
                tf = tf.name.split('\\')
                print(tf)
                with open("./saved/"+tf[len(tf)-1],"wb") as myfile:
                    pickle.dump(unpick, myfile)
                print("Saved")
                window.savedtab()

#Window by Christopher Scott
class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.tabs = QTabWidget(self)
        # self.tabs.setTabsClosable(True)
        layout = QGridLayout(self)
        layout.addWidget(self.tabs, 0, 0, 1, 2)
        self.tab1 = Homepage()
        self.tabs.addTab(self.tab1,"Home")
        self.tab2 = savedpage()
        self.tabs.addTab(self.tab2,"Saved")
    #this creates the result tab
    def createNewTab(self,imgs):
        
        #DELETE OLD TAB
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == 'Results':
                self.tabs.removeTab(i)

        index = self.tabs.count()
        self.tabs.addTab(resultpage(), 'Results')
        self.tabs.setCurrentIndex(index)
        self.tabs.update()
    #this creates the saved tab
    def savedtab(self):
        #DELETE OLD TAB
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == 'Saved':
                self.tabs.removeTab(i)
        
        index = self.tabs.count()
        self.tabs.addTab(savedpage(), 'Saved')
        self.tabs.setCurrentIndex(index)
        self.tabs.update()
    #this creates the edit tab
    def paintTab(self,img):
        #DELETE OLD TAB
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == 'Edit':
                self.tabs.removeTab(i)
        
        index = self.tabs.count()
        self.tabs.addTab(ImageManipulation(img), 'Edit')
        self.tabs.setCurrentIndex(index)
        self.tabs.update()
    #Deprecated
    def repaint(self):
        #redrawing tab
        self.tabs.currentWidget().repaint()



#Homepage by Bobby Davis
class Homepage(QWidget):
    def __init__(self):
        super().__init__()

        # Declare Widgets
        self.homepage_label = QLabel('Home')
        self.search_label = QLabel('Find an Image!')
        self.srch_box = QLineEdit() # input field for search
        self.srch_btn = QPushButton("Search")

        # Create U.I. Layout
        mbox = QVBoxLayout() # Main layout

        vbox = QVBoxLayout()    # Layout for search feature
        vbox.addWidget(self.homepage_label)
        vbox.addWidget(self.search_label)
        vbox.addWidget(self.srch_box)
        vbox.addWidget(self.srch_btn)

        gbox1 = QGroupBox() # Set group for search feature layout
        gbox1.setLayout(vbox)
        mbox.addWidget(gbox1)

        # Home Images
        images = []
        images = self.getHomepageImages()

        # Create layout for images
        vbox2 = QHBoxLayout()   # horizontal layout

        i = 0
        for img in images:  # iterate through images list
            self.label = QLabel()

            pixmap1 = QPixmap(img)  # set image
            pixmap1 = pixmap1.scaled(300, 300, Qt.KeepAspectRatio)

            self.label.setPixmap(pixmap1)

            temp_vbox = QVBoxLayout()
            temp_vbox.addWidget(self.label)  

            gbox2 = QGroupBox() # group box for current image
            gbox2.setLayout(temp_vbox)
            gbox2.setStyleSheet("background-color: grey")
            
            vbox2.addWidget(gbox2)
            i += 1

        gbox3 = QGroupBox() # main group box for images
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

        payload = { # pass parameters
            'client_id': api_key,
            'query' : self.srch_box.text(),
            'page' : 1,
            'per_page' : 1
        }
        endpoint = 'https://api.unsplash.com/search/photos' # define endpoint
        try:
            request = requests.get(endpoint, params=payload)
            data = request.json()
            pprint(data)
        except:
            print('please try again')

        if data:    # iterate through retrieved json object
            i = 0
            imgs = []
            for image in data['results']:
                im = Image.open(requests.get(image['urls']['full'], stream=True).raw)   # get image from json
                imgs.append(image)
                with open("./results/result"+str(i),"wb") as myfile:
                    pickle.dump(image, myfile)
                name = "./results/result"+str(i)+".jpg"
                i += 1
            window.createNewTab(imgs)
        else:
            print('no data')

    def getHomepageImages(self):
        home_images = []
        print("Finding Match...")

        payload = {
            'client_id': api_key,
            'count' : 3
        }
        endpoint = 'https://api.unsplash.com/photos/random' # use this endpoint for random images
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
#ImageManipulation by Cody Todd
class ImageManipulation(QWidget):
    def __init__(self,img):
        super().__init__()

        # Declare Widgets
        self.edit_label = QLabel('Change your image')

        # set up list and combo box option
        self.my_list = ["Pick a value", "Luminosity", "Contrast", "Colorize", "Sepia", "Negative", "Grayscale", "None"]
        self.my_combo_box = QComboBox()
        self.my_combo_box.addItems(self.my_list)

        self.edit_btn = QPushButton("Edit")

        # Create U.I. Layout
        mbox = QHBoxLayout()

        vbox = QVBoxLayout()
        vbox.addWidget(self.edit_label)
        vbox.addWidget(self.my_combo_box)
        vbox.addWidget(self.edit_btn)

        mbox.addLayout(vbox)
        image = Image.open(requests.get(img['urls']['thumb'], stream=True).raw)
        editpath = "./editing/edit.jpg"
        image.save(editpath)
        self.lbl = QLabel()
        pix = QPixmap(editpath)
        self.lbl.setPixmap(pix)
        mbox.addWidget(self.lbl)
        

        self.setLayout(mbox) # apply layout to this class

        # when button is clicked send lineedit and combo box info to on_submit
        self.edit_btn.clicked.connect(self.on_edit)

    @Slot()
    def on_edit(self):

        # set up im_edit as which filter the user chose
        im_edit = self.my_combo_box.currentText()

        # take the image to edit and load it
        input_image = Image.open("./editing/edit.jpg")
        input_pixels = input_image.load()

        output_image = Image.new("RGB", input_image.size)
        draw = ImageDraw.Draw(output_image)

        # Options are: ["Pick a value", "Luminosity", "Contrast", "Colorize", "Sepia", "Negative", "Grayscale", "None"]
        # Luminostity brightens the image overall
        if (im_edit == "Luminosity"):
            luminosity = 80

            # Generate image
            for x in range(output_image.width):
                for y in range(output_image.height):
                    r, g, b = input_pixels[x, y]
                    r = int(r + luminosity)
                    g = int(g + luminosity)
                    b = int(b + luminosity)
                    draw.point((x, y), (r, g, b))

                    
            output_image.show()
        # Contrast makes the image slightly darker overall
        elif (im_edit == "Contrast"):
            # Find minimum and maximum luminosity
            imin = 255
            imax = 0
            for x in range(input_image.width):
                for y in range(input_image.height):
                    r, g, b = input_pixels[x, y]
                    i = (r + g + b) / 3
                    imin = min(imin, i)
                    imax = max(imax, i)

            # Generate image
            for x in range(output_image.width):
                for y in range(output_image.height):
                    r, g, b = input_pixels[x, y]
                    # Current luminosity
                    i = (r + g + b) / 3
                    # New luminosity
                    ip = 255 * (i - imin) / (imax - imin)
                    r = int(r * ip / i)
                    g = int(g * ip / i)
                    b = int(b * ip / i)
                    draw.point((x, y), (r, g, b))

            output_image.show()
        # Colorize increases one color in the image
        elif (im_edit == "Colorize"):
            # Square distance between 2 colors
            def distance2(color1, color2):
                r1, g1, b1 = color1
                r2, g2, b2 = color2
                return (r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2

            color_to_change = (0, 0, 255)
            threshold = 220

            # Generate image
            for x in range(output_image.width):
                for y in range(output_image.height):
                    r, g, b = input_pixels[x, y]
                    if distance2(color_to_change, input_pixels[x, y]) < threshold ** 2:
                        r = int(r * .5)
                        g = int(g * 1.25)
                        b = int(b * .5)
                    draw.point((x, y), (r, g, b))

            output_image.show()
        # Sepia increases the red and decreases the blue value depending on the intensity
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
            output_image.show()
        # Negative swaps the rgb values to their opposite counterparts
        elif (im_edit == "Negative"):
            negative_list = [(255-p[0], 255-p[1], 255-p[2])
                                for p in input_image.getdata()]
            output_image.putdata(negative_list)
            output_image.show()
        # Grayscale averages the rgb values and creates the gray version of the image
        elif (im_edit == "Grayscale"):
            new_list = [ ( (a[0]+a[1]+a[2])//3, ) * 3
                                for a in input_image.getdata() ]
            output_image.putdata(new_list)
            output_image.show()
        else: #"Pick a value" or "None"
            input_image.show()



if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(800, 150, 650, 500)
    window.show()
    sys.exit(app.exec_())
