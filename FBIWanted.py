#!/usr/bin/python3

# Author:	ramb0
# Name:		FBIWanted.py
# Description:	Handles FBI database file/API calls.

import requests, json, pickle, os, sys, datetime
from enum import Enum
MAX_PAGE_SIZE = 50

class FBIWanted():

        databaseFile = ""
        totalOfEntries = 0
        FBI_DATA = []

        def __init__(self, databaseFile, updateDB):
                self.databaseFile = databaseFile
                self.updateDB = updateDB
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

                # If we force to update the file.
                if self.updateDB == True:
                        print("[...] Outdated FBI database! Downloading now...")
                        os.remove(self.databaseFile)

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

                        print("[!] Database file '%s' succesfully updated!" % self.databaseFile)
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

                print("[!] Database file '%s' succesfully updated!" % self.databaseFile)
                self.entryParser = self.EntryParser(self.FBI_DATA)
                return True

        # Parses the entries by their specifications.
        class EntryParser:

                def __init__(self, FBI_DATA):
                        self.FBI_DATA = FBI_DATA

                # All possible subjects.
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
                        PARENTAL_KIDNAPPING_VICTIM = "Parental Kidnapping Victim"
                        CHINA_THREAT = "China Threat"
                        LAW_ENFORCEMENT_ASSISTANCE = "Law Enforcement Assistance"
                        OPERATION_LEGEND = "Operation Legend"
                        TEN_MOST_WANTED =  "Ten Most Wanted Fugitives"
                        MOST_WANTED_TERRORISTS = "Most Wanted Terrorists"
                        COUNTERINTELLIGENCE = "Counterintelligence"
                        HUMAN_TRAFFICKING = "Human Trafficking"
                        CRIMES_AGAINST_CHILDREN = "Crimes Against Children"
                        KNOWN_BANK_ROBBERS = "Known Bank Robbers"
                        DOMESTIC_TERRORISM = "Domestic Terrorism"
                        OTHER = "Other unlisted subjects"

                # Lists all the available subjects to search for.
                def listAllSubjects(self):

                        print("[!] All Subjects listed:\n")
                        counter = 0
                        for Subj in (self.Subject):
                                print("[%-2d] %-45s %s" % (counter, str(Subj), Subj.value))
                                counter += 1
                        print()

                # Get count of cases per subject.
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
                        
                        # Check if subject exists.
                        exists = False
                        for subj in self.Subject:
                                if str(subj) == subject:
                                        subject = subj
                                        exists = True
                                        break
                                
                        if exists == False:
                                print("[!] The given subject "+ subject + " does not exists!")
                                return


                        print("[...] Searching for subject entries with '" + subject.value + "'\n")
                       
                        for i in range (0, len(self.FBI_DATA)):

                                person = self.FBI_DATA[i]

                                # If an person has no subject.
                                if len(person['subjects']) == 0:
                                        continue

                                # Iterate over all subjects from person.
                                for j in range(0, len(person['subjects'])):
                                        
                                        # Match the subjects.
                                        if person['subjects'][j] == subject.value:
                                                ID = person['@id'][person['@id'].rfind('/') +1:]
                                                print("%-30s %s" % (self.FBI_DATA[i]['title'], ID))

                # Get entry based on title.
                def getEntryOnTitle(self, title):

                        print("[...] Searching for title '" + title + "'\n")

                        for i in range(0, len(self.FBI_DATA)):

                                person = self.FBI_DATA[i]

                                # Check if title corresponds.
                                if person['title'].upper().find(title.upper()) != -1:
                                        self.printProfile(person)
                                        continue

                                # Find title in alias
                                if person['aliases'] == None:
                                        continue

                                for alias in person['aliases']:
                                        if alias.upper().find(title.upper()) != -1:
                                                self.printProfile(person)

                # Get entries with a bounty.
                def getBountyEntries(self):
                        print("[...] Searching for entries with a bounty\n")


                        counter = 0
                        for i in range(0, len(self.FBI_DATA)):

                                person = self.FBI_DATA[i]

                                if person['reward_text'] != None:
                                        self.printProfile(person)
                                        counter +=1

                        print("\nFound %d entries!" % counter)

                # Get the profile with the ID.
                def getProfileByID(self, ID):

                        print("[...] Searching profile with ID %s" % ID)

                        for i in range(0, len(self.FBI_DATA)):
                                person = self.FBI_DATA[i]

                                if person['@id'] == ID:
                                        self.printProfile(person)
                                        return
                                elif person['@id'][person['@id'].rfind('/') +1:] == ID:
                                        self.printProfile(person)
                                        return

                        print("[!] Profile ID not found in database!\n")

                # The sorting function.
                def sortingOnDateTime(self, e):
                        return datetime.datetime.strptime(e['publication'], "%Y-%m-%dT%H:%M:%S")

                # Get the latest records
                def getLatestRecords(self):

                        print("[...] Get the latest profiles")

                        # Sort from high to low.
                        self.FBI_DATA.sort(reverse=True, key=self.sortingOnDateTime)

                        for i in range(0, 5):
                                print(self.printProfile(self.FBI_DATA[i]))

                # Get the pictures from an ID.
                def getPictureByID(self, ID):
                        print("[...] Get the links of the pictures from a profile\n")

                        # Get the profile object from the list.
                        personProfile = ""
                        for i in range(0, len(self.FBI_DATA)):
                                person = self.FBI_DATA[i]

                                if person['@id'] == ID:
                                        personProfile = person
                                        break
                                elif person['@id'][person['@id'].rfind('/') +1:] == ID:
                                        personProfile = person
                                        break
                        if personProfile == "":
                                print("[!] Profile ID not detected!\n")
                                return

                        for i in range(0, len(personProfile['images'])):
                                
                                if personProfile['images'][i]['caption'] != None:
                                        print("Caption: " + personProfile['images'][i]['caption'])
                                
                                if personProfile['images'][i]['original'] != None:
                                        print("Original: " + personProfile['images'][i]['original'])
                                
                                if personProfile['images'][i]['thumb'] != None:
                                        print("Thumbnail: " + personProfile['images'][i]['thumb'])
                                
                                if personProfile['images'][i]['large'] != None:
                                        print("Large: " + personProfile['images'][i]['large'])
                                print()
                                
                # Get the important information about this person.
                def printProfile(self, person):

                        print("]]]]]]  %s  [[[[[[" % person['title'])
                        if person['warning_message'] != None:
                                print("WARNING:\t%s " % person['warning_message'])

                        if person['reward_text'] != None:
                                print("BOUNTY:\t\t%s" % person['reward_text'])

                        print("ID:\t\t%s  %s" % (person['@id'][person['@id'].rfind('/') +1:], person['@id']))
                        print("Public since:\t%s" % datetime.datetime.strptime(person['publication'], "%Y-%m-%dT%H:%M:%S"))

                        if person['modified'] != None:
                                print("Modified:\t%s" % datetime.datetime.strptime(person['modified'], "%Y-%m-%dT%H:%M:%S+00:00"))

                        if person['aliases'] != None:
                                for alias in person['aliases']:
                                        print("Alias:\t\t%s" % alias)

                        # Information about himself
                        print("Description:")
                        print("  Sex:         %s" % person['sex'] )
                        print("  Hair:        %s" % person['hair'])
                        print("  Eyes:        %s" % person['eyes'])
                        print("  Weight:      %s" % person['weight'])
                        print("  Weight max:  %s" % person['weight_max'])
                        print("  Race:        %s" % person['race_raw'])
                        print("  Age:         %s" % person['age_range'])
                        print("  Min height:  %s" % person['height_min'])
                        print("  Max height:  %s" % person['height_max'])

                        if person['scars_and_marks'] != None:
                                print("  Scars/marks: %s" % person['scars_and_marks'])

                        if person['images'] != None:
                                print("  Image count: %d" % len(person['images']))
 

                        print()

                        # More information about the person.
                        print("Additional information:")
                        
                        if person['occupations'] != None:
                                for occupation in person['occupations']:
                                        print("Occupation:\t%s" % occupation)

                        if person['dates_of_birth_used'] != None:
                                for birth in person['dates_of_birth_used']:
                                        print("Birth:\t\t%s" % birth)

                        if person['place_of_birth'] != None:
                                print("Place birth:\t%s" % person['place_of_birth'])


                        if person['nationality'] != None:
                                print("Nationality:\t%s" % person['nationality'])

                        if person['possible_countries'] != None:
                                for country in person['possible_countries']:
                                        print("Pot. country:\t%s" % country)

                        print("Subjects:\t", end="")
                        if person['subjects'] != None:
                                for subject in person['subjects']:
                                        print("%s | " % subject, end="")
                                print()

                        if person['remarks'] != None:
                                print("Remarks:\t%s" % person['remarks'])

                        if person['details'] != None:
                                print("Details:\t%d bytes" % len(person['details']))

                        if person['caution'] != None:
                                print("Caution: \n\n%s" % person['caution'])
                        print()

#FBI_DB = WantedFBI('databaseFBI.csv')
#if FBI_DB.getAllEntriesFromList() == False:
        #sys.exit(1)

#FBI_DB.entryParser.getEntryOnTitle("palmer")

#FBI_DB.entryParser.listAllSubjects()

#BI_DB.entryParser.getEntryCountPerSubject()

#FBI_DB.entryParser.getSubjectEntries(FBI_DB.entryParser.Subject.TEN_MOST_WANTED)

#print(FBI_DB.entryParser.Subject.MISSING_PERSON)
