import sys
from PySide6.QtWidgets import QGroupBox, QListWidgetItem,QMainWindow, QGridLayout, QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QDialog, QTextBrowser, QComboBox, QLineEdit, QTabWidget, QListWidget, QListView
from PySide6.QtCore import Qt, Slot, QSize, Signal, QObject
from PySide6.QtGui import QPixmap, QIcon
from PIL import Image
import requests, json
from pprint import pprint
import os, pickle
import tempfile


class savedpage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        i = 0
        self.names = []
        self.ebutons = []
        self.dbutons = []
        folder = './saved'
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
                im = Image.open(requests.get(imag['cover_photo']['urls']['thumb'], stream=True).raw)
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
        print("saving "+self.names[button])
        folder = './saved'
        
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
                with open("./saved/saved"+str(i),"wb") as myfile:
                    #pickle.dump(unpick, myfile)
                    print("")
                print("Saved")
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
                
                        



class resultpage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        i = 0
        self.names = []
        self.ebutons = []
        folder = './results'
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
                im = Image.open(requests.get(imag['cover_photo']['urls']['thumb'], stream=True).raw)
                im.save(path)
                self.ebutons[i] = QPushButton("Save result"+str(i+1))
                self.ebutons[i].clicked.connect(lambda state=i, a=i:self.saveme(state))
                pixmap = QPixmap(path)
                self.image = QLabel()
                self.image.setPixmap(pixmap)
                lay.addWidget(self.image)
                lay.addWidget(self.ebutons[i])
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
    def saveme(self,button):
        print("saving "+self.names[button])
        folder = './results'
        
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

    def createNewTab(self,imgs):
        
        #DELETE OLD TAB
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == 'Results':
                self.tabs.removeTab(i)

        index = self.tabs.count()
        self.tabs.addTab(resultpage(), 'Results')
        self.tabs.setCurrentIndex(index)
        self.tabs.update()

    def savedtab(self):
        #DELETE OLD TAB
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == 'Saved':
                self.tabs.removeTab(i)
        
        index = self.tabs.count()
        self.tabs.addTab(savedpage(), 'Saved')
        self.tabs.setCurrentIndex(index)
        self.tabs.update()

    def repaint(self):
        #redrawing tab
        self.tabs.currentWidget().repaint()


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
        print("clearing old results")
        folder = './results'
        for filename in os.listdir(folder):
            path = folder + "/" + filename
            try:
                if os.path.isfile(path) or os.path.islink(path):
                    os.unlink(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

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
            i = 0
            imgs = []
            for image in data['results']:
                im = Image.open(requests.get(image['cover_photo']['urls']['full'], stream=True).raw)
                imgs.append(image)
                with open("./results/result"+str(i),"wb") as myfile:
                    pickle.dump(image, myfile)
                name = "./results/result"+str(i)+".jpg"
                #im.save(name)
                # with open("./results/result"+str(i),"rb") as my_file:
                #     unpick = pickle.load(my_file)
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