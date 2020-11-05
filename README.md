# FBI-wanted-list
I found an API from the FBI, where you can see the list of people they are searching for. I tought it was cool if I created a tool that interacts with this API. We can search for names and prices on people's head.

## How it works
The API receives a few objects: 'total','items','page'. Here the total object gives the count of 
entries of the list. In the items object we have to actual data of the persons in the list and the
page gives the pagenumber, like in a book.  

The script first requests the data from the FBI API and stores it into a local file. This is where
the data will be stored until the remote database is updated. In the list we have for every person
a subject, the reason why the person is wanted. The title gives usually the name of the person.  

The possible subjects are:
```
[0 ] Subject.CYBER_MOST_WANTED                     Cyber's Most Wanted
[1 ] Subject.SEEKING_INFO                          Seeking Information
[2 ] Subject.SEEKING_INFO_TERRORISM                Seeking Information - Terrorism
[3 ] Subject.WHITE_COLLAR_CRIME                    White-Collar Crime
[4 ] Subject.VICAP_HOMICIDE_SEXUAL_ASSAULT         ViCAP Homicides and Sexual Assaults
[5 ] Subject.VICAP_MISSING_PERSON                  ViCAP Missing Persons
[6 ] Subject.VICAP_UNIDENTIFIED_PERSONS            ViCAP Unidentified Persons
[7 ] Subject.KIDNAPPING_MISSING_PERSON             Kidnappings and Missing Persons
[8 ] Subject.ENDANGERED_CHILD_PROGRAM              Endangered Child Alert Program
[9 ] Subject.VIOLENT_CRIME_MURDER                  Violent Crimes - Murders
[10] Subject.VIOLENT_CRIME_OTHER                   Additional Violent Crimes
[11] Subject.CASE_OF_WEEK                          Case of the Week
[12] Subject.CRIMINAL_ENTERPRISE_INVESTIGATION     Criminal Enterprise Investigations
[13] Subject.ECAP                                  ECAP
[14] Subject.JOHN_DOE                              John Doe
[15] Subject.PARENTAL_KIDNAPPING                   Parental Kidnapping
[16] Subject.PARENTAL_KIDNAPPING_VICTIM            Parental Kidnapping Victim
[17] Subject.CHINA_THREAT                          China Threat
[18] Subject.LAW_ENFORCEMENT_ASSISTANCE            Law Enforcement Assistance
[19] Subject.OPERATION_LEGEND                      Operation Legend
[20] Subject.TEN_MOST_WANTED                       Ten Most Wanted Fugitives
[21] Subject.MOST_WANTED_TERRORISTS                Most Wanted Terrorists
[22] Subject.COUNTERINTELLIGENCE                   Counterintelligence
[23] Subject.HUMAN_TRAFFICKING                     Human Trafficking
[24] Subject.CRIMES_AGAINST_CHILDREN               Crimes Against Children
[25] Subject.KNOWN_BANK_ROBBERS                    Known Bank Robbers
[26] Subject.DOMESTIC_TERRORISM                    Domestic Terrorism
```

## Screenshot
![Screenshot](https://github.com/Trisna22/FBI-wanted-list/blob/main/screenshot.png)

## Script
In the script I created you can search for subjects, names (title), bounties and id.

## Graphical User Interface
In the GUI you can also search for subjects, names (title), publication/modification dates and more. We used the tkinter libary in python3.

## Usage
```
Usage: main.py [options]

Options:
  -h, --help            show this help message and exit
  -t TITLE, --title=TITLE
                        search for title
  -s SUBJECT, --subjects=SUBJECT
                        search for subject
  -f FILENAME, --file=FILENAME
                        the database file to use
  -u, --update          update the database file
  -l, --list-subjects   lists all subjects
  -n, --list-subjectnums
                        list subjects with count of entries
  -a, --list-all        lists all profiles
  -b, --bounty          lists all profiles with a reward
  -i ID, --id=ID        print profile based on id
```
