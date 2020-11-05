import tkinter
from tkinter import ttk 
from tkinter import messagebox
import datetime
from PIL import ImageTk, Image

import FBIWanted # Our FBI class
import PersonInfo # Our PersonInfo class

# MVC MODEL
#https://wiki.wxpython.org/ModelViewController

class FBIWantedGUI():
        mainWindow = tkinter.Tk()

        def create_window(self):
                self.controller = self.Controller(self.mainWindow)
                self.controller.load_components()

        class Controller:

                def __init__(self, mainWindow):
                        self.mainWindow = mainWindow
                        self.mainWindow.minsize(1000, 600)
                        self.mainWindow.geometry("1000x600")
                        self.mainWindow.title("FBI wanted list")
                        
                        # FBI database object.
                        self.FBI_DATA = FBIWanted.FBIWanted()
                        self.databaseFile = "FBI_Database.dat"

                def load_components(self):
                        self.view = self.View(self.mainWindow)

                        # Add commands to buttons.
                        self.view.getMenuFileMenu().add_command(label="Create database from API", command=self.createDatabase)
                        self.view.getMenuFileMenu().add_command(label="Import database", command=self.importDatabase)
                        self.view.getMenuFileMenu().add_command(label="Close database", command=self.closeDatabase)

                        # Add command to treeview items.
                        self.view.getTreeview().bind("<Double-1>", self.treeviewDoubleClick)
                        self.view.getTreeview().bind("<<TreeviewSelect>>", self.treeviewSelect)

                        self.mainWindow.mainloop()

                # Double click on treeview item.
                def treeviewDoubleClick(self, event):
                        
                        # Check if treeview is empty.
                        if self.view.getTreeview().selection() == ():
                                return

                        # Get the ID.
                        item = self.view.getTreeview().selection()[0]
                        ID = self.view.getTreeview().item(item, "text")

                        status = self.FBI_DATA.getPersonByID(ID)
                        if status['code'] != 1:
                                messagebox.showwarning("Warning",str(status['reason']))
                                return

                        personInfo = PersonInfo.PersonInfo(self.mainWindow, ID, status['person'])

                # When the selection of the treeview changes.
                def treeviewSelect(self, event):
                        # Check if treeview is empty.
                        if self.view.getTreeview().selection() == ():
                                return

                        # Get the ID.
                        item = self.view.getTreeview().selection()[0]
                        ID = self.view.getTreeview().item(item, "text")

                        # Get the path of the picture.
                        status = self.FBI_DATA.getPictureByID(ID)
                        if status['code'] != 1:
                                return
                        
                        # Set the picture.
                        image = Image.open(status['fileName'])
                        image = image.resize((300, 400), Image.ANTIALIAS)
                        img = ImageTk.PhotoImage(image)
                        self.view.getImageCanvas().create_image(0, 0, anchor=tkinter.NW, image=img)
                        self.view.getImageCanvas().image = img

                        # Set the ID.
                        self.view.getIdLabel().config(text =ID)

                        # Get the title based on te ID.
                        status = self.FBI_DATA.getPersonByID(ID)
                        if status['code'] != 1:
                                return

                        # Set the title
                        self.view.getTitleLabel().config (text=status['person']['title'])

                        # Set the subjects.
                        subjects = ""
                        for subject in status['person']['subjects']:
                                subjects += subject + " | "
                        self.view.getSubjectLabel().config(text=subjects)

                def closeDatabase(self):
                        print("Close Database clicked!")

                # When menu button import database is clicked.
                def importDatabase(self):
                        print("Import database clicked!")
                
                # When menu button create database is clicked.
                def createDatabase(self):

                        # Let the FBIWanted class do the loading.
                        status = self.FBI_DATA.loadDatabase(self.databaseFile)
                        if status['code'] != 1:
                                messagebox.showwarning("Warning",str(status['reason']))
                                return
                        
                        # Insert all records into our treeview.
                        data = self.FBI_DATA.getFBIData()
                        for i in range(0, len(data)):

                                person = data[i]
                                ID = person['@id'][person['@id'].rfind('/') +1:]
                                PUBLIC = datetime.datetime.strptime(person['publication'], "%Y-%m-%dT%H:%M:%S")
                                
                                self.view.getTreeview().insert("", "end", text=ID, values=(ID, person['title'], str(PUBLIC)))
                     
                        messagebox.showinfo("Success", "FBI database downloaded succesfully!\n" + str(len(data)) + " records collected!")

                class View:
                        def __init__(self, mainWindow):
                                self.mainWindow = mainWindow

                                # Add menu
                                self.menu = tkinter.Menu(self.mainWindow)
                                self.mainWindow.config(menu=self.menu)

                                # File menu
                                self.fileMenu = tkinter.Menu(self.menu, tearoff=0)
                                self.menu.add_cascade(label="File", menu=self.fileMenu)

                                # Create our treeview list.
                                self.treeview = self.createTreeview()

                                # Create an image holder.
                                self.imageCanvas = self.createImage()

                                # Label for ID, title and subjects
                                self.idLabel = tkinter.Label(self.mainWindow)
                                self.titleLabel = tkinter.Label(self.mainWindow)
                                self.subjectLabel = tkinter.Label(self.mainWindow)
                                self.titleLabel.place(x=700, y=450)
                                self.idLabel.place(x=700, y=475)
                                self.subjectLabel.place(x=700, y=500)
                                
                        # Creates a treeview control.
                        def createTreeview(self):
                                treeview = ttk.Treeview(self.mainWindow, selectmode='browse', height=20, columns=("0", "1", '2'))
                                treeview['show'] = 'headings' # Get rid of identifier column
                                treeview.place(x=20, y=20)
                                # Treeview headers
                                treeview.heading("0", text="ID")
                                treeview.heading("1", text="Title")
                                treeview.heading("2", text="Publication")

                                # Columns
                                treeview.column("0", width = 100, stretch=True) 
                                treeview.column("1", width = 300, stretch=True) 
                                treeview.column("2", width = 200, stretch=True) 

                                # TODO: Add styling with ttk.Style() and tag='default-style' 
                                #treeview.configure('none', background="White", foreground="Black")
                                return treeview

                        # Creates an canvas for our image to appear.
                        def createImage(self):
                                imageCanvas = tkinter.Canvas(self.mainWindow, width=300, height=400)
                                imageCanvas.place(x=675, y=20)
                                return imageCanvas

                        def getMenuFileMenu(self):
                                return self.fileMenu

                        def getTreeview(self):
                                return self.treeview

                        def getImageCanvas(self):
                                return self.imageCanvas

                        def getIdLabel(self):
                                return self.idLabel

                        def getTitleLabel(self):
                                return self.titleLabel

                        def getSubjectLabel(self):
                                return self.subjectLabel

app = FBIWantedGUI()
app.create_window()
