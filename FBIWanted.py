#!/usr/bin/python3

# Author:	ramb0
# Name:		FBIWantedList.py
# Description:	Handles FBI database file/API calls.

import requests, json, pickle, os, sys
from enum import Enum
MAX_PAGE_SIZE = 50

#https://api.fbi.gov/@wanted
class WantedFBI:

        databaseFile = ""
        totalOfEntries = 0
        FBI_DATA = []

        def __init__(self, databaseFile):
                self.databaseFile = databaseFile
                self.totalOfEntries = self.getTotalEntries()
                self.entryParser = self.EntryParser(None)
                print("[%] FBI entry count " + str(self.totalOfEntries))

        # Make a request to the API.
        def requestList(self, pageSize, pageNumber):
                response = requests.get('https://api.fbi.gov/@wanted?pageSize=' + str(pageSize) +
                        '&page=' + str(pageNumber))
                if response.status_code != 200:
                        print("\nRequest with size %d on page number %d failed!" % (pageSize, pageNumber))
                        return "ERROR " + str(response.status_code)

                return json.loads(response.content)['items']

        # Retrieve the total of entries of the wanted list.
        def getTotalEntries(self):
                response = requests.get('https://api.fbi.gov/@wanted')
                if response.status_code != 200:
                        print("\nRequest with size %d on page number %d failed!" % (pageSize, pageNumber))
                        return -1

                return int(json.loads(response.content)['total'])

        # Check if there is an database file stored locally.
        def checkLocalDBFile(self):
                try:
                        f = open(self.databaseFile, 'rb')
                        return True
                except IOError:
                        return False

        # Retrieve all entries from database.
        def getAllEntriesFromList(self):

                print("[...] Collecting FBI data...")
                self.FBI_DATA.clear()

                # Check if the database already is stored locally.
                if self.checkLocalDBFile() == True:

                        print("[...] Reading database from file...")

                        # Get the database from the file.

                        try:
                                with open(self.databaseFile, 'rb') as fp:
                                        self.FBI_DATA = pickle.load(fp)
                        except EOFError:
                                print("[-] Invalid database file!")
                                return False
                        except IOError:
                                print("[-] Input/Output error!")
                                return False

                        if len(self.FBI_DATA) != self.totalOfEntries:
                                print("[...] Outdated FBI database! Downloading now...")
                                os.remove(self.databaseFile)
                                return self.getAllEntriesFromList()

                        print("[!] Database file succesfully updated!")
                        self.entryParser = self.EntryParser(self.FBI_DATA)
                        return True

                # Get the database from the API.
                entryNumber = 0
                pageNumber = 0

                print("[...] Reading database from API...")

                while entryNumber < self.totalOfEntries:

                        # Check if we are at the last entry.
                        if (self.totalOfEntries - entryNumber) < 50:
                                self.FBI_DATA.extend(self.requestList(self.totalOfEntries - entryNumber, pageNumber))

                        # Else get the dataset of 25 entries.
                        self.FBI_DATA.extend(self.requestList(MAX_PAGE_SIZE, pageNumber))
                        pageNumber += 1
                        entryNumber += 50

                if len(self.FBI_DATA) != self.totalOfEntries:
                        print("[-] Partial collection of FBI database! Count: %d" % (len(self.FBI_DATA)))

                # Write the content to file.
                print("[...] Write database to file...")
                with open(self.databaseFile, 'wb') as fp:
                        pickle.dump(self.FBI_DATA, fp)

                print("[!] Database file succesfully updated!")
                self.entryParser = self.EntryParser(self.FBI_DATA)
                return True

        def getSubjectEntries(self):
                print(EntryParser.Subject().CYBER_MOST_WANTED)
                
        # Parses the entries by their specifications.
        class EntryParser:

                def __init__(self, FBI_DATA):
                        self.FBI_DATA = FBI_DATA

                class Subject(Enum):
                        CYBER_MOST_WANTED = "Cyber's Most Wanted"
                        SEEKING_INFO = "Seeking Information"
                        SEEKING_INFO_TERRORISM = "Seeking Information - Terrorism"
                        WHITE_COLLAR_CRIME = "White-Collar Crime"
                        VICAP_HOMICIDE_SEXUAL_ASSAULT = "ViCAP Homicides and Sexual Assaults"
                        VICAP_MISSING_PERSON = "ViCAP Missing Persons"
                        VICAP_UNIDENTIFIED_PERSONS = "ViCAP Unidentified Persons"
                        KIDNAPPING_MISSING_PERSON = "Kidnappings and Missing Persons"
                        ENDANGERED_CHILD_PROGRAM = "Endangered Child Alert Program"
                        VIOLENT_CRIME_MURDER = "Violent Crimes - Murders"
                        VIOLENT_CRIME_OTHER = "Additional Violent Crimes"
                        CASE_OF_WEEK = "Case of the Week"
                        CRIMINAL_ENTERPRISE_INVESTIGATION = "Criminal Enterprise Investigations"
                        ECAP = "ECAP"
                        JOHN_DOE = "John Doe"
                        PARENTAL_KIDNAPPING = "Parental Kidnapping"
                        CHINA_THREAT = "China Threat"
                        LAW_ENFORCEMENT_ASSISTANCE = "Law Enforcement Assistance"
                        OPERATION_LEGEND = "Operation Legend"
                        TEN_MOST_WANTED =  "Ten Most Wanted Fugitives"
                        MOST_WANTED_TERRORISTS = "Most Wanted Terrorists"
                        COUNTERINTELLIGENCE = "Counterintelligence"
        

                def listAllSubjects(self):

                        print("[!] All Subjects listed:\n")
                        counter = 0
                        for Subj in (self.Subject):
                                print("[%-2d] %-45s %s" % (counter, str(Subj), Subj.value))
                                counter += 1
                        print()

                def getEntryCountPerSubject(self):

                        print("[!] Entry count for every subject:\n")

                        totalCount = 0
                        for Subj in (self.Subject):

                                counter = 0
                                for i in range(0, len(self.FBI_DATA)):
                                        person = self.FBI_DATA[i]
                                        
                                        for j in range(0, len(person['subjects'])):
                                                if person['subjects'][j] == Subj.value:
                                                        counter += 1
                                print("%-40s %d" % (Subj.value, counter))
                                totalCount += counter

                        print("\nTotal of " + str(totalCount) + " entries.\n")

                # Get the entry based on subject.
                def getSubjectEntries(self, subject):
                        
                        print("[...] Searching for entries with '" + subject.value + "'\n")

                        for i in range (0, len(self.FBI_DATA)):

                                person = self.FBI_DATA[i]

                                # If an person has no subject.
                                if len(person['subjects']) == 0:
                                        continue

                                # Iterate over all subjects from person.
                                for j in range(0, len(person['subjects'])):
                                        
                                        # Match the subjects.
                                        if person['subjects'][j] == subject.value:
                                                print(self.FBI_DATA[i]['title'])

                

FBI_DB = WantedFBI('databaseFBI.csv')
if FBI_DB.getAllEntriesFromList() == False:
        sys.exit(1)

FBI_DB.entryParser.listAllSubjects()

FBI_DB.entryParser.getEntryCountPerSubject()

#FBI_DB.entryParser.getSubjectEntries(FBI_DB.entryParser.Subject.MOST_WANTED_TERRORISTS)

#print(FBI_DB.entryParser.Subject.MISSING_PERSON)