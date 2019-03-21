idoc_search
 
Created by Eric Hyatt
Last updated: 12/12/2018
_______________________________________________________________________________

This tool allows the user to perform a search on EDI documents that have been
recieved, withtin a user specified date range.

This program is intended to be used with Fabri-Kal's Gentran setup. This
program will not likely work if Gentran's file system is changed or directory
names are updated.


_______________________________________________________________________________
TO INSTALL:

Unzip the idco_search_dist.zip file if you haven't already.

1) Create the Search folder: C:\GENSRVNT\Search
2) Copy the idoc_search_dist folder to a permanent location

The program should run fine wherever the dist folder is (as long as the 
C:\GENSRVNT\IntIn\ folder exists), though the results will not be printed to a 
file if the C:\GENSRVNT\Search folder does not exist.


_______________________________________________________________________________
TO USE:

Open the program by finding the idoc_search.exe file in the
idoc_search_dist\idoc_serach folder. There may be a shortcut to open this file
already created.

A Command Prompt window will open. You will be asked to enter a 'Start Date'
once the program opens. Followed by a request for an 'End Date'.

After that you will be able to specify a search term. This can be anything
you'd like (partner number, order number, ect.). The program will look for
this term within all the idocs (EDI documents) that were recieved within the
specified date range.

The results will be shown in the Command Prompt window, as well as being
printed to a file and stored in the C:\GENSRVNT\Search\ folder.

You'll then have the option to perform another search.


_______________________________________________________________________________
POSSIBLE ERRORS:

ERROR: 'Please enter a valid date.'
Dates need to be in a valid format. The program has directions and error
messages to handle this. 

Error: 'THERE WAS AN ERROR WRITTING TO LOG FILE.'
There may be an issue writting the results file to the Search folder. This is
ususally because the folder doesn't exist, or is not where it's expected to
be. The folder MUST be accurately named and in the correct enclosing folder:
C:\GENSRVNT\Search\

For errors not handled in the program, the source code may need to be updated.
See the DEVELOPER_README.txt file for more info.