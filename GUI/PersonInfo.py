import tkinter
from tkinter import ttk
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

                # Description 
                self.createDescription()

                # Warning message
                if person['warning_message'] != None:
                        tkinter.Message(self.profileWindow, text=str(person['warning_message']),fg="Red", justify=tkinter.LEFT, width=400).place(x=350, y=250)

                # Caution box
                #self.createCautionbox()

                # Bounty label
                tkinter.Label(self.profileWindow, text="Bounty:").place(x=350, y=300)
                if person['reward_text'] != None:
                        tkinter.Message(self.profileWindow, text=person['reward_text'], justify=tkinter.LEFT, bg="Black", fg="White", borderwidth=2, width=300).place(x=425, y=300)
                else:
                        tkinter.Label(self.profileWindow, text="None").place(x=425, y=300)

                        
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

        # Creates the description of the person.
        def createDescription(self):
                tkinter.Label(self.profileWindow, text="Sex:").place(x=350, y=60)
                tkinter.Label(self.profileWindow, text="Hair:").place(x=350, y=80)
                tkinter.Label(self.profileWindow, text="Eyes:").place(x=350, y=100)
                tkinter.Label(self.profileWindow, text="Weight:").place(x=350, y=120)
                tkinter.Label(self.profileWindow, text="Weight max:").place(x=350, y=140)
                tkinter.Label(self.profileWindow, text="Race:").place(x=350, y=160)
                tkinter.Label(self.profileWindow, text="Age:").place(x=350, y=180)
                tkinter.Label(self.profileWindow, text="Min height:").place(x=350, y=200)
                tkinter.Label(self.profileWindow, text="Max height:").place(x=350, y=220)

                tkinter.Label(self.profileWindow, text=str(self.person['sex'])).place(x=450, y=60)
                tkinter.Label(self.profileWindow, text=str(self.person['hair'])).place(x=450, y=80)
                tkinter.Label(self.profileWindow, text=str(self.person['eyes'])).place(x=450, y=100)
                tkinter.Label(self.profileWindow, text=str(self.person['weight'])).place(x=450, y=120)
                tkinter.Label(self.profileWindow, text=str(self.person['weight_max'])).place(x=450, y=140)
                tkinter.Label(self.profileWindow, text=str(self.person['race_raw'])).place(x=450, y=160)
                tkinter.Label(self.profileWindow, text=str(self.person['age_range'])).place(x=450, y=180)
                tkinter.Label(self.profileWindow, text=str(self.person['height_min'])).place(x=450, y=200)
                tkinter.Label(self.profileWindow, text=str(self.person['height_max'])).place(x=450, y=220)

        # Creates the box for the caution of person.
        def createCautionbox(self):
                container = ttk.Frame(self.profileWindow, height= 100)
                canvas = tkinter.Canvas(container)

                scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
                scrollable_frame = ttk.Frame(canvas)
                scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                        scrollregion=canvas.bbox("all")
                ))

                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

                canvas.configure(yscrollcommand=scrollbar.set)
        
                tkinter.Message(scrollable_frame, text=str(self.person['caution'])).pack()

                container.place(x=350, y=250)
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")





