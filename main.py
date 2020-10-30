from optparse import OptionParser

import FBIWanted
import sys

parser = OptionParser()
parser.add_option("-t", "--title", help="search for title", dest="TITLE", default=None)
parser.add_option("-s", "--subjects", help="search for subject", dest="SUBJECT", default=None)
parser.add_option("-f", "--file", help="the database file to use", dest="FILENAME", default="databaseFBI.csv")
parser.add_option("-u", "--update", help="update the database file", dest="UPDATE", action="store_true", default=False)
parser.add_option("-l", "--list-subjects", help="lists all subjects", dest="LIST_SUBJECTS", action="store_true", default=False)
parser.add_option("-n", "--list-subjectnums", help="list subjects with count of entries", dest="LIST_SUBJECT_ENTRY", action="store_true", default=False)
parser.add_option("-a", "--list-all", help="lists all profiles", dest="LIST_ALL", action="store_true", default=False)
parser.add_option("-b", "--bounty", help="lists all profiles with a reward", dest="BOUNTY", action="store_true", default=False)
parser.add_option("-i", "--id", help="print profile based on id", dest="ID", default=None)
parser.add_option("-d", "--latest", help="get the latest records", dest="LATEST", action="store_true", default=False)

(options, args) = parser.parse_args()

wanted = FBIWanted.FBIWanted(options.FILENAME, options.UPDATE)

if wanted.getAllEntriesFromList() == False:
        sys.exit(1)

# Check if the user wants to list any information.
if options.LIST_SUBJECTS == True:
        wanted.entryParser.listAllSubjects()
        sys.exit(0)

if options.LIST_SUBJECT_ENTRY == True:
        wanted.entryParser.getEntryCountPerSubject()
        sys.exit(0)

if options.BOUNTY == True:
        wanted.entryParser.getBountyEntries()
        sys.exit(0)

if options.LATEST == True:
        wanted.entryParser.getLatestRecords()
        sys.exit(0)

if options.SUBJECT != None:
        wanted.entryParser.getSubjectEntries(options.SUBJECT)
        sys.exit(0)

if options.TITLE != None:
        wanted.entryParser.getEntryOnTitle(options.TITLE)
        sys.exit(0)

if options.ID != None:
        wanted.entryParser.getProfileByID(options.ID)
        sys.exit(0)


print("No action given!\n")