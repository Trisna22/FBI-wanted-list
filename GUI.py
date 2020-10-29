
import tkinter

class FBIWantedGUI():
	mainWindow = tkinter.Tk()

	def create_window(self):
		self.mainWindow.minsize(800, 600)
		self.mainWindow.geometry("800x600")
		self.mainWindow.mainloop()


app = FBIWantedGUI()
app.create_window()
