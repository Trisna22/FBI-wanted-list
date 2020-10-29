#!/usr/bin/python3

# Author:	ramb0
# Name:		FBIWantedList.py
# Description:	Find information about the FBI's wanted list.

import requests, json, pickle

MAX_PAGE_SIZE = 50

allPersons = []

# Make a request to the API.
def requestList(pageSize, pageNumber):
	response = requests.get('https://api.fbi.gov/@wanted?pageSize=' + str(pageSize) +
		'&page=' + str(pageNumber))
	if response.status_code != 200:
		print("\nRequest with size %d on page number %d failed!" % (pageSize, pageNumber))
		return "ERROR " + str(response.status_code)

	return json.loads(response.content)['items']

# Retrieve the total of entries of the wanted list.
def getTotalEntries():
	response = requests.get('https://api.fbi.gov/@wanted')
	if response.status_code != 200:
		print("\nRequest with size %d on page number %d failed!" % (pageSize, pageNumber))
		return -1

	return int(json.loads(response.content)['total'])

# Check if there is an database file stored locally.
def checkLocalDBFile(fileName):

	try:
		f = open(fileName, 'rb')
		return True
	except IOError:
		return False

# Retrieve all entries from database.
def getAllEntriesFromList(databaseFile, totalOfEntries):

	FBI_DATA = []

	# Check if the database already is stored locally.
	if checkLocalDBFile(databaseFile) == True:

		print("[...] Reading database from file...")

		# Get the database from the file.
		with open(databaseFile, 'rb') as fp:
			FBI_DATA = pickle.load(fp)

		if len(FBI_DATA) != totalOfEntries:
	                print("[-] Partial collection of FBI database! Count: %d" % (len(FBI_DATA)))
		return FBI_DATA

	# Get the database from the API.
	entryNumber = 0
	pageNumber = 0

	print("[...] Reading database from API...")

	while entryNumber < totalOfEntries:

		# Check if we are at the last entry.
		if (totalOfEntries - entryNumber) < 50:
			FBI_DATA.extend(requestList(totalOfEntries - entryNumber, pageNumber))

		# Else get the dataset of 25 entries.
		FBI_DATA.extend(requestList(MAX_PAGE_SIZE, pageNumber))
		pageNumber += 1
		entryNumber += 50

	if len(FBI_DATA) != totalOfEntries:
		print("[-] Partial collection of FBI database! Count: %d" % (len(FBI_DATA)))

	# Write the content to file.
	print("[...] Write database to file...")
	with open(databaseFile, 'wb') as fp:
		pickle.dump(FBI_DATA, fp)
	return FBI_DATA

def main():
	# Check if API is accessible.
	totalOfEntries = getTotalEntries()
	if totalOfEntries == -1:
		print("\nFailed to receive total of entries!")
		print("API not accessible! QUITTING.\n")
		return

	print("[%] FBI entry count " + str(totalOfEntries))
	print("[...] Collecting FBI data...")

	FBI_DATA = getAllEntriesFromList('FBIWanted_db.csv', totalOfEntries)
	if FBI_DATA == None:
		print("[-] Failed to read the FBI database!")
		return

	print("[...] Sorting FBI data")
#	for i in range(0, len(FBI_DATA)):

#		print(FBI_DATA[i]['title'])

#		print(str(person.keys()))
#		print(str(person['title']))
#		print(str(person['@id']))
#		print(str(person['subjects']))
#		print("\n")


if __name__ == "__main__":
	main()


