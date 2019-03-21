idoc_search
 
Created by Eric Hyatt
Last updated: 12/12/2018
_______________________________________________________________________________
Written in Python 3.7
Modules used: datetime, os, datetime.timedelta, pandas

pyinstaller was used to create the dist folder, including the .exe file used to 
run the program.

There are hidden files in the idoc_serach_dist folder including:
  installer batch file for moving dist folder and creating Search folder more 
    easily (don't use if you don't know what you're doing!)
  icon image
  source code for editing/review (copy then edit!)
  setup batch file for creating the dist folder (pyinstaller command)

_______________________________________________________________________________
This program was written very specifically for the current (2018) Fabri-Kal EDI 
system. Any changes to this system could break the program. Specifically the 
hard coded file paths throughout the program. If these directories move or are 
renamed, the program will not function properly. Simply updating the file 
paths may fix the issue. 

If changes are made to the source code the program will need to be build again 
if you would like an executable to run the program. This can be accomplished by 
using pyinstaller. There are many ways to accomplish this but this is what was 
used originally. 
There is a batch file that runs the original pyinstaller script. Updating the 
file paths should allow you to run this batch file and create the dist folder 
again. Be sure to look up and read the pyinstaller documentation for more details.  


_______________________________________________________________________________
If you're reading this and I (Eric) no longer work at Fabri-Kal, feel free to try and contact me for assistance. No promises, but I'll probably be willing to help!
