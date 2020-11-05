#!/usr/bin/python3

# Author:	ramb0
# Name:		FBIWanted.py
# Description:	Handles FBI database file/API calls.

import requests, json, pickle, os, sys, datetime
from enum import Enum
import urllib.request
import tkinter
import tkinter.ttk as ttk

class FBIWanted:

        def __init__(self):
                self.databaseFile = ""
                self.totalOfEntries = 0
                self.FBI_DATA = []
                        
        # Check if connection with the API is available.
        def __checkIfConnectionAvailable(self):
                try:
                        r = requests.head("https://api.fbi.gov/", timeout=3)
                        return True
                except requests.ConnectionError as ex:
                        return False

        # Get count of total entries from API.
        def __getTotalOfEntries(self):

                if self.__checkIfConnectionAvailable():
                        response = requests.get('https://api.fbi.gov/@wanted')
                        if response.status_code != 200:
                                return -1
                        return int(json.loads(response.content)['total'])
                return 0
        
        # Check if there is an database file stored locally.
        def __checkLocalDBFile(self):
                try:
                        f = open(self.databaseFile, 'rb')
                        return True
                except IOError:
                        return False
        
        # Load the database 
        def loadDatabase(self, fileName):
                self.databaseFile = fileName

                # Get the total count of entries.
                self.totalOfEntries = self.__getTotalOfEntries()

                # Check if database is saved locally.
                if self.__checkLocalDBFile() == False:
                        print("Database file doesn't exists!")
                        if self.__checkIfConnectionAvailable() == False:
                                return {'code':0, 'reason':'No database file or connection available!'}

                        return self.__loadDatabase_API()
                return self.__loadDatabase_FILE()

        # Load the database from the API.
        def __loadDatabase_API(self):
                
                entryNumber = 0
                pageNumber = 0

                # Create progressbar window.
                master = tkinter.Tk()
                master.minsize(300, 60)
                master.geometry("300x60")
                master.wm_attributes('-type', 'splash')
                master.title("Downloading FBI data...")

                # Progressbar
                progressBar = ttk.Progressbar(master, orient="horizontal",
                        mode="determinate", maximum=100, value=0, length=200)
                progressBar.place(x=20, y=20)
                progressBar['value'] = 0

                # Label
                label = tkinter.Label(master, text="Downloading FBI data...")
                label.place(x=50, y=40)
                master.update()

                while entryNumber < self.totalOfEntries:

                        # Check if we are at the last entry.
                        if (self.totalOfEntries - entryNumber) < 50:
                                self.FBI_DATA.extend(self.__requestList(self.totalOfEntries - entryNumber,pageNumber))
   
                        # Else get the dataset of 50 entries.
                        self.FBI_DATA.extend(self.__requestList(50, pageNumber))
                        pageNumber += 1
                        entryNumber += 50

                        # Update the progressbar
                        progressBar['value'] = entryNumber / self.totalOfEntries * 100
                        master.update()

                master.destroy()
                try:
                        # Write content to file.
                        with open(self.databaseFile, 'wb') as fp:
                                pickle.dump(self.FBI_DATA, fp)
                except:
                        return {'code':0, 'reason':'Failed to write content to file'}
                return {'code': 1, 'reason': 'success'}
                
        # Read the database from existing file.
        def __loadDatabase_FILE(self):
                # Get the database from the file.
                try:
                        with open(self.databaseFile, 'rb') as fp:
                                self.FBI_DATA = pickle.load(fp)

                        # Check if the database file is outdated.
                        if len(self.FBI_DATA) < self.totalOfEntries and self.__checkIfConnectionAvailable():
                                print("Database file outdated!")
                                os.remove(self.databaseFile)
                                self.FBI_DATA.clear()
                                return self.__loadDatabase_API() # Get the new data from the API.

                        self.totalOfEntries = len(self.FBI_DATA)

                        return {'code':1, 'reason':'success'}
                except EOFError:
                        print("[-] Invalid database file!")
                        return {'code':2, 'reason': 'Database file has an invalid format!'}
                except IOError:
                        print("[-] Input/Output error!")
                        return {'code':0, 'reason': 'Failed to read the database file!' }
                
        # Read a page from the API.
        def __requestList(self, pageSize, pageNumber):
                response = requests.get('https://api.fbi.gov/@wanted?pageSize=' + str(pageSize) +
                        '&page=' + str(pageNumber))
                if response.status_code != 200:
                        print("\nRequest with size %d on page number %d failed!" % (pageSize, pageNumber))
                        return "ERROR " + str(response.status_code)

                return json.loads(response.content)['items']


        def getFBIData(self):
                return self.FBI_DATA
                
        # Get the person's records based on ID.
        def getPersonByID(self, ID):
                
                # Loop trough records.
                for i in range(0, len(self.FBI_DATA)):
                        person = self.FBI_DATA[i]

                        if person['@id'] == ID:
                                return {'code':1, 'person':person}

                        elif person['@id'][person['@id'].rfind('/') +1:] == ID:
                                return {'code':1, 'person':person}

                return {'code':0, 'reason':'ID not found in database!'}

        # Writes an image of the ID to a file.
        def __writeToFile(self, url, ID):

                # Check if the image file already exists.
                if os.path.exists(ID + ".orig"):
                        return True

                # Download the file from database.
                if not self.__checkIfConnectionAvailable():
                        return False

                try:
                        r = requests.get(url)
                        with open(ID + ".orig", "wb") as f:
                                f.write(r.content)

                        return True
                except:
                        return False

        # Get the person's picture based on ID.
        def getPictureByID(self, ID):

                # To prevent too much network usage, we're gonna save the files.
                for i in range(0, len(self.FBI_DATA)):
                        person = self.FBI_DATA[i]

                        if person['@id'][person['@id'].rfind('/') +1:] == ID:
                                if self.__writeToFile(person['images'][0]['original'], ID) == False:
                                        return {'code': 0, 'reason':'Failed to download the image from database!'}
                                else:
                                        return {'code': 1, 'fileName': ID + ".orig"}

                return {'code':0, 'reason':'ID not found in database!'}


        def getCriminalWithID(self, ID):

                return {'code':0, 'reason':"Connection with FBI API not available!"}

                
                