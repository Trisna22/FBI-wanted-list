import tkinter
from tkinter import ttk 
from tkinter import messagebox
import datetime

import FBIWanted # Our FBI class

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
                        self.mainWindow.minsize(1200, 600)
                        self.mainWindow.geometry("1200x600")
                        self.mainWindow.title("FBI wanted list")
                        
                        # FBI database object.
                        self.FBI_DATA = FBIWanted.FBIWanted()
                        self.databaseFile = "FBI_Database.dat"

                def load_components(self):
                        self.view = self.View(self.mainWindow)

                        # Add commands to buttons.
                        self.view.getMenuFileMenu().add_command(label="Import database", command=self.importDatabase)
                        self.view.getMenuFileMenu().add_command(label="Close database", command=self.closeDatabase)
                        self.view.getMenuFileMenu().add_command(label="Create database from API", command=self.createDatabase)

                        # Add command to treeview items.
                        self.view.getTreeview().bind("<Double-1>", self.treeviewDoubleClick)

                        self.mainWindow.mainloop()

                # Double click on treeview item.
                def treeviewDoubleClick(self, event):
                        
                        # Check if treeview is empty.
                        if self.view.getTreeview().selection() == ():
                                return

                        # Get the ID.
                        item = self.view.getTreeview().selection()[0]
                        ID = self.view.getTreeview().item(item, "text")

                        # Create new window with this item showing.
                        profileWindow = tkinter.Toplevel(self.mainWindow)
                        profileWindow.minsize(600, 500)

                        labelID = tkinter.Label(profileWindow, text="ID:")
                        labelID2 = tkinter.Label(profileWindow, text=ID)
                        labelID.place(x=20, y=20)
                        labelID2.place(x=20, y=50)

                        #FBI_DB.getProfileOnID(item.getID())
                def closeDatabase(self):
                        print("Close Database clicked!")

                def importDatabase(self):
                        print("Import database clicked!")

                def createDatabase(self):

                        # Let the FBIWanted class do the loading.
                        status = self.FBI_DATA.loadDatabase(self.databaseFile)
                        if status['code'] != 1:
                                messagebox.showwarning("Warning",str(status['reason']))
                        
                        # Insert all records into our treeview.
                        data = self.FBI_DATA.getFBIData()
                        for i in range(0, len(data)):

                                person = data[i]
                                ID = person['@id'][person['@id'].rfind('/') +1:]
                                PUBLIC = datetime.datetime.strptime(person['publication'], "%Y-%m-%dT%H:%M:%S")
                                
                                self.view.getTreeview().insert("", "end", text=ID, values=(ID, person['title'], str(PUBLIC)))
                     
                        messagebox.showinfo("Success", "FBI database downloaded succesfully!\n" + len(data) + " records collected!")

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

                        # Creates a treeview control.
                        def createTreeview(self):
                                treeview = ttk.Treeview(self.mainWindow, selectmode='browse', height=20, columns=("0", "1", '2', "3"))
                                treeview['show'] = 'headings' # Get rid of identifier column
                                treeview.place(x=20, y=20)
                                # Treeview headers
                                treeview.heading("0", text="ID")
                                treeview.heading("1", text="Title")
                                treeview.heading("2", text="Publication")
                                treeview.heading("3", text="Subject")
                                # Columns
                                treeview.column("0", width = 100, stretch=True) 
                                treeview.column("1", width = 300, stretch=True) 
                                treeview.column("2", width = 200, stretch=True) 
                                treeview.column("3", width = 300, stretch=True) 

                                # TODO: Add styling with ttk.Style() and tag='default-style' 
                                #treeview.configure('none', background="White", foreground="Black")
                                return treeview
          
                        def getMenuFileMenu(self):
                                return self.fileMenu

                        def getTreeview(self):
                                return self.treeview

app = FBIWantedGUI()
app.create_window()
