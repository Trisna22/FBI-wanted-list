import tkinter
from PIL import Image, ImageTk
import datetime

class PersonInfo:

        def __init__(self, mainWindow, ID, person):
                self.ID = ID
                self.person = person

                # Create new window with this item showing.
                self.profileWindow = tkinter.Toplevel(mainWindow)
                self.profileWindow.minsize(800, 600)

                # ID Label
                tkinter.Label(self.profileWindow, text="ID:").place(x=20, y=450)
                tkinter.Label(self.profileWindow, text=ID).place(x=60, y=450)

                # Title Label
                tkinter.Label(self.profileWindow, text="Title:").place(x=20, y=475)
                tkinter.Label(self.profileWindow, text=person['title']).place(x=60, y=475)

                # Publication label
                PUBLIC = datetime.datetime.strptime(person['publication'], "%Y-%m-%dT%H:%M:%S")
                tkinter.Label(self.profileWindow, text="Publication:").place(x=20, y=500)
                tkinter.Label(self.profileWindow, text=PUBLIC).place(x=100, y=500)

                # Modified label
                if person['modified'] != None:
                        MODIFIED = datetime.datetime.strptime(person['modified'], "%Y-%m-%dT%H:%M:%S+00:00")
                        tkinter.Label(self.profileWindow, text="Modified:").place(x=20, y=525)
                        tkinter.Label(self.profileWindow, text=MODIFIED).place(x=100, y=525)

                # Subjects label
                if person['subjects'] != None:
                        subjects = ""
                        for subject in person['subjects']:
                                subjects += subject + " | "
                        
                        tkinter.Label(self.profileWindow, text="Subjects:").place(x=350, y=40)
                        tkinter.Label(self.profileWindow, text=subjects).place(x=425, y=40)

                # Bounty label
                tkinter.Label(self.profileWindow, text="Bounty:").place(x=350, y=65)
                if person['reward_text'] != None:
                        tkinter.Label(self.profileWindow, text=person['reward_text']).place(x=425, y=65)


                self.createImage()

                
        # Creates the image from our person.
        def createImage(self):

                imageCanvas = tkinter.Canvas(self.profileWindow, width=300, height=400)
                imageCanvas.place(x=20, y=20)
                image = Image.open(self.ID + ".orig")
                image = image.resize((300, 400), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(image)
                imageCanvas.create_image(0, 0, anchor=tkinter.NW, image=img)
                imageCanvas.image = img


