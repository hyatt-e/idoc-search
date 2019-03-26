import datetime
import os
from datetime import timedelta
import pandas

# GLOBAL VARIABLES #
doctype = None
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']


# CLASSES #


class Output:
    search_dir = ''
    log_dir = ''

    error = 0
    status = ''
    exit = False
    validStartDt = False
    validEndDt = False


class Search:
    startDate = ''
    endDate = ''
    searchStr = ''
    dateRange = None
    numFiles = 0
    dirs = []
    paths = []
    paths2 = []
    outputA = {}
    outputR = {}
    unknown = {}
    validDocList = {}
    invalidDocs = 0


# updated 1/8/19
def future_date_chk(inDate):
    # convert date string into date object
    inDate = datetime.datetime.strptime(inDate, '%m-%d-%Y').date()
    # if inDate > datetime.date.today().strftime('%m-%d-%Y'):
    if inDate > datetime.date.today():
        return 4
    else:
        return 0


def start_end_chk(start, end):
    d1 = datetime.datetime.strptime(start, "%m-%d-%Y").date()
    d2 = datetime.datetime.strptime(end, "%m-%d-%Y").date()
    if d2 < d1:
        return 3
    else:
        return 0


def format_date(date, separator):
    if separator == '':
        month = date[:2]
        day = date[2:4]
        year = date[4:]
    else:
        try:
            month, day, year = date.split(separator)
        except ValueError:
            searchStatus.error = 1
            error_msg(searchStatus, searchMain)

    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day
    if len(year) == 2:
        # if year is greater than current year, assume it's a 20th cent. year
        if year > datetime.datetime.today().strftime('%y'):
            year = '19' + year
        else:
            year = '20' + year
    elif len(year) < 2:
        # year is missing or too short
        searchStatus.error = 2

        error_msg(searchStatus, searchMain)

    # replace separators with '-'
    date = month + '-' + day + '-' + year
    return date


def vali_date(searchMain, searchStatus):
    # ensure dates are valid
    # check date is in past
    # check that start date is before end
    start = searchMain.startDate
    end = searchMain.endDate
    error = 0

    if end == '':
        error = future_date_chk(start)
        if error != 0:
            return error

        stMonth, stDay, stYear = start.split('-')
        print(months[int(stMonth) - 1], stDay + ',', stYear + '\n')
        return error

    elif end != '':
        error = future_date_chk(end)
        if error != 0:
            return error

        error = start_end_chk(start, end)
        if error != 0:
            return error

        endMonth, endDay, endYear = end.split('-')
        print(months[int(endMonth) - 1], endDay + ',', endYear + '\n')
        return error


def set_date_rng(searchStatus, searchMain):
    # print status; print errors, if any
    searchStatus.error = 0
    searchStatus.status = 1
    searchStatus.exit = False
    status_output(searchStatus, searchMain)

    while searchStatus.exit is False:
        if searchStatus.validStartDt is False:
            # set and print default date
            defaultStart = datetime.date.today() - timedelta(1)
            defaultStart = defaultStart.strftime('%m-%d-%Y')
            print('\n')
            print('[{}]'.format(defaultStart))

            # Take input for start date
            searchMain.startDate = input("Start Date: ") or defaultStart

            if searchMain.startDate.lower() == "exit":
                searchStatus.exit = True
                searchStatus.error = 000
                error_msg(searchStatus, searchMain)
            elif searchMain.startDate.lower() == "date":
                # RESTART
                restart(searchStatus, searchMain)
            elif len(searchMain.startDate) > 10 or len(searchMain.startDate) < 6:
                # input date too short
                searchStatus.error = 2
                error_msg(searchStatus, searchMain)
            else:
                # find separator; reformat date; make sure date is valid
                if '\\' in searchMain.startDate:
                    separator = '\\'
                    # convert any single digit numbers; make all separators -
                    searchMain.startDate = \
                        format_date(searchMain.startDate, separator)
                    searchStatus.error = vali_date(searchMain, searchStatus)
                    # check for error
                    if searchStatus.error != 0:
                        error_msg(searchStatus, searchMain)
                    else:
                        searchStatus.validStartDt = True

                elif '/' in searchMain.startDate:
                    separator = '/'
                    # convert any single digit numbers; make all separators -
                    searchMain.startDate = \
                        format_date(searchMain.startDate, separator)
                    searchStatus.error = vali_date(searchMain, searchStatus)
                    # check for error
                    if searchStatus.error != 0:
                        error_msg(searchStatus, searchMain)
                    else:
                        searchStatus.validStartDt = True

                elif '-' in searchMain.startDate:
                    separator = '-'
                    # convert any single digit numbers; make all separators -
                    searchMain.startDate = \
                        format_date(searchMain.startDate, separator)
                    searchStatus.error = vali_date(searchMain, searchStatus)
                    # check for error
                    if searchStatus.error != 0:
                        error_msg(searchStatus, searchMain)
                    else:
                        searchStatus.validStartDt = True

                elif '.' in searchMain.startDate:
                    separator = '.'
                    # convert any single digit numbers; make all separators -
                    searchMain.startDate = \
                        format_date(searchMain.startDate, separator)
                    searchStatus.error = vali_date(searchMain, searchStatus)
                    # check for error
                    if searchStatus.error != 0:
                        error_msg(searchStatus, searchMain)
                    else:
                        searchStatus.validStartDt = True

                elif len(searchMain.startDate) == 8:
                    separator = ''
                    # convert any single digit numbers; make all separators -
                    searchMain.startDate = \
                        format_date(searchMain.startDate, separator)
                    searchStatus.error = vali_date(searchMain, searchStatus)
                    # check for error
                    if searchStatus.error != 0:
                        error_msg(searchStatus, searchMain)
                    else:
                        searchStatus.validStartDt = True

                else:
                    # no seperators and not 8 digits
                    searchStatus.error = 2
                    error_msg(searchStatus, searchMain)

        elif searchStatus.validEndDt is False:
            status_output(searchStatus, searchMain)

            # set and print default date
            defaultEnd = datetime.date.today().strftime('%m-%d-%Y')
            print('\n')
            print('[{}]'.format(defaultEnd))

            # Take input for end date
            searchMain.endDate = input("End Date: ") or defaultEnd

            if searchMain.endDate.lower() == "exit":
                searchStatus.exit = True
                searchStatus.error = 000
                error_msg(searchStatus, searchMain)
            elif searchMain.endDate.lower() == "date":
                # RESTART
                restart(searchStatus, searchMain)
            # rough length check
            elif len(searchMain.endDate) > 10 or len(searchMain.endDate) < 6:
                # input date too short
                searchStatus.error = 2
                error_msg(searchStatus, searchMain)

            # check for single digit numbers and add 0's
            else:
                # find separator; reformat date; make sure date is valid
                if '\\' in searchMain.endDate:
                    separator = '\\'
                    # convert any single digit numbers; make all separators -
                    searchMain.endDate = \
                        format_date(searchMain.endDate, separator)
                    searchStatus.error = vali_date(searchMain, searchStatus)
                    # check for error
                    if searchStatus.error != 0:
                        error_msg(searchStatus, searchMain)
                    else:
                        searchStatus.validEndDt = True

                elif '/' in searchMain.endDate:
                    separator = '/'
                    # convert any single digit numbers; make all separators -
                    searchMain.endDate = \
                        format_date(searchMain.endDate, separator)
                    searchStatus.error = vali_date(searchMain, searchStatus)
                    # check for error
                    if searchStatus.error != 0:
                        error_msg(searchStatus, searchMain)
                    else:
                        searchStatus.validEndDt = True

                elif '-' in searchMain.endDate:
                    separator = '-'
                    # convert any single digit numbers; make all separators -
                    searchMain.endDate = \
                        format_date(searchMain.endDate, separator)
                    searchStatus.error = vali_date(searchMain, searchStatus)
                    # check for error
                    if searchStatus.error != 0:
                        error_msg(searchStatus, searchMain)
                    else:
                        searchStatus.validEndDt = True

                elif '.' in searchMain.endDate:
                    separator = '.'
                    # convert any single digit numbers; make all separators -
                    searchMain.endDate = \
                        format_date(searchMain.endDate, separator)
                    searchStatus.error = vali_date(searchMain, searchStatus)
                    # check for error
                    if searchStatus.error != 0:
                        error_msg(searchStatus, searchMain)
                    else:
                        searchStatus.validEndDt = True

                elif len(searchMain.endDate) == 8:
                    separator = ''
                    # convert any single digit numbers; make all separators -
                    searchMain.endDate = \
                        format_date(searchMain.endDate, separator)
                    searchStatus.error = vali_date(searchMain, searchStatus)
                    # check for error
                    if searchStatus.error != 0:
                        error_msg(searchStatus, searchMain)
                    else:
                        searchStatus.validEndDt = True

                else:
                    # no seperators and not 8 digits
                    searchStatus.error = 2
                    error_msg(searchStatus, searchMain)

        if searchStatus.error != 0:
            error_msg(searchStatus, searchMain)
        elif searchStatus.validEndDt is True:
            searchStatus.exit = True

    searchMain.dateRange = pandas.date_range(start=searchMain.startDate,
                                             end=searchMain.endDate)
    searchMain.dateRange = pandas.Series(searchMain.dateRange.format())

    return searchMain.dateRange, searchMain.startDate, searchMain.endDate


def create_paths(searchMain):
    # turn dates into paths
    paths = []
    for date in searchMain.dateRange:
        year, month, day = date.split('-')
        paths.append(searchStatus.search_dir + '#{}\\{}\\{}\\'
                     .format(year, month, day))
    return paths


def find_dir(searchMain):
    # find all directories associated with date range
    paths2 = []
    for path in searchMain.paths:
        try:
            os.chdir(path)
            # path exists
            good_path = True
        except FileNotFoundError:
            # paths.remove(path)
            good_path = False

        # if the path exists, get all directories within it
        if good_path is True:
            dirs = os.listdir()
            for dirty in dirs:
                paths2.append(path + dirty + '\\')

    return paths2


def string_search(searchStatus, searchMain):
    searchStatus.status = 3
    status_output(searchStatus, searchMain)

    searchMain.searchStr = input('').lower()
    if searchMain.searchStr.lower() == "exit":
        searchStatus.exit = True
        searchStatus.error = 000
        error_msg(searchStatus, searchMain)
    elif searchMain.searchStr.lower() == "date":
        restart(searchStatus, searchMain)

    elif searchMain.searchStr == '':
        searchStatus.error = 5
        error_msg(searchStatus, searchMain)

    searchStatus.status = 4
    status_output(searchStatus, searchMain)

    for path in searchMain.paths2:
        searchMain.numFiles = searchMain.numFiles + len(os.listdir(path))

        for file in os.listdir(path):
            # Search all dirs within these paths
            docPath = path + file
            file = open(docPath)
            file = file.read().lower()

            if searchMain.searchStr.lower() in file:
                matching_lines = []
                matching_lines = find_lines(file, matching_lines, searchMain)
                searchMain.validDocList[docPath] = matching_lines
            else:
                searchMain.invalidDocs += 1

            status_output(searchStatus, searchMain)

    return searchMain.invalidDocs, searchMain.validDocList


def find_lines(file, matching_lines, searchMain):
    # separate lines of idoc.
    lines = file.split("~")

    # Search each line for string. If line is found to contain the string, add
    # line and file to log
    line_num = 0
    for line in lines:
        line_num += 1
        if searchMain.searchStr in line:
            matching_lines.append("Line " + str(line_num) + ": " + line)
            continue

    return matching_lines


# Output Strings #
no_docs_msg = ("No idoc's containing the search criteria found in this date range.\n")

search_str_msg = "\nEnter a search term bellow.\n"

date_rng_msg = "Date Range: "

use_dt_msg = "Enter 'S' to perform a different search within the same date range."

close_restart_msg = "Enter 'DATE' to use a new date range,\nor 'EXIT' to close the program.\n"

instruction_msg1 = ("Please enter dates with the month, followed by day, followed by year."
                    "\nUse . - \\ / or no separators (must be MMDDYYYY) between month, day and year.")

default_dt_msg = "Press 'Enter' to use the [Default Date]."

case_irrelevant_msg = ("This is not case sensitive (capital letters will be lower-cased).")

file_not_found_msg = ("Could not open the US Foods Control Numbers document!"
                      "\nMake sure the file is in the correct location:"
                      "\n'G:\\WPy-3661\\python\\USF-997\\US Foods Control Numbers.csv'")

no_dir_for_range = ("No directories were found matching this date range."
                    "\nThere may be no inbound files for the specified dates.")

invalidDate_msg1 = "Please enter a valid date.\n"

seperator_msg = ("Dates may use . - \\ / or no separators may be used to separate month, day, and year. "
                    "Dates without seperators must be an 8 digit long, fortmated as MMDDYYYY."
                    "\n(ie. March 9, 1994 as 03091994).")

date_too_short = "Your entry is either too long, or too short to be a date.\n"

end_b4_st_msg = "The End Date must be later than the Start Date.\n"

future_dt_msg = "You cannot select a date that is in the future.\n"

blank_entry_msg = "Your entry was blank.\n"

log_write_error_msg = ('THERE WAS AN ERROR WRITTING TO LOG FILE.\n'
                       "Make sure the 'C:\\GENSRVNT\\Search\\' directoy exists.\n")

exit_msg = "BYE!"
# ___________________________________________________________________________#


def restart(searchStatus, searchMain):
    # could assert valid start and end date
    print('\r')

    # RESTART
    if searchStatus.status != 5:
        # don't clear screen; leave summary displayed
        os.system('cls')

    if searchMain.startDate.lower() == "date" or \
       searchMain.endDate.lower() == "date" or \
       searchMain.searchStr.lower() == "date" or \
       searchStatus.error == 6:

        searchStatus.search_dir = ''
        searchStatus.log_dir = ''
        searchStatus.error = 0
        searchStatus.status = ''
        searchStatus.exit = False
        searchStatus.validStartDt = False
        searchStatus.validEndDt = False

        searchMain.startDate = ''
        searchMain.endDate = ''
        searchMain.searchStr = ''
        searchMain.dateRange = None
        searchMain.numFiles = 0
        searchMain.dirs = []
        searchMain.paths = []
        searchMain.paths2 = []
        searchMain.outputA = {}
        searchMain.outputR = {}
        searchMain.unknown = {}
        searchMain.validDocList = {}
        searchMain.invalidDocs = 0

        main_loop(searchStatus, searchMain)

    print(date_rng_msg + searchMain.startDate + ' to ' + searchMain.endDate)

    print('\n')
    print("Would you like to perform another search?")
    print("\n")
    print(use_dt_msg)
    print(close_restart_msg)
    restart = input('')

    if restart.lower() == 's':
        searchStatus.error = 0
        searchStatus.status = 1
        searchStatus.exit = False

        searchMain.searchStr = ''
        searchMain.numFiles = 0
        searchMain.outputA = {}
        searchMain.outputR = {}
        searchMain.unknown = {}
        searchMain.validDocList = {}
        searchMain.invalidDocs = 0

        main_loop(searchStatus, searchMain)

    elif restart.lower() == "date":
        searchStatus.search_dir = ''
        searchStatus.log_dir = ''
        searchStatus.error = 0
        searchStatus.status = ''
        searchStatus.exit = False
        searchStatus.validStartDt = False
        searchStatus.validEndDt = False

        searchMain.startDate = ''
        searchMain.endDate = ''
        searchMain.searchStr = ''
        searchMain.dateRange = None
        searchMain.numFiles = 0
        searchMain.dirs = []
        searchMain.paths = []
        searchMain.paths2 = []
        searchMain.outputA = {}
        searchMain.outputR = {}
        searchMain.unknown = {}
        searchMain.validDocList = {}
        searchMain.invalidDocs = 0

        main_loop(searchStatus, searchMain)

    elif restart.lower() == 'exit':
        searchStatus.error = 000
        error_msg(searchStatus, searchMain)
    else:
        # bad input; repeat message
        status_output(searchStatus, searchMain)


def reuse_start(searchStatus, searchMain):
    if searchStatus.validStartDt is True:
        os.system('cls')
        print('Start Date:')
        print(searchMain.startDate)
        print('\n')
        response = input('Would you like to use this start date? [y/N]\n')
        if response.lower() == 'n':
            searchStatus.validStartDt = False
        elif response.lower() == 'y':
            searchStatus.validStartDt = True
        elif response.lower() == 'exit':
            searchStatus.error = 000
            error_msg(searchStatus, searchMain)
        else:
            # bad input; repeat error msg
            error_msg(searchStatus, searchMain)
        searchStatus.error = 0
        main_loop(searchStatus, searchMain)
    else:
        searchStatus.error = 0
        main_loop(searchStatus, searchMain)


def status_output(searchStatus, searchMain):
    # control output
    # display info and instructions through out program

    if searchStatus.status == 1:
        status_msg = "SELECT DATE RANGE . . ."
        os.system('cls')
        print(status_msg)
        print('\n')
        print(instruction_msg1 + '\n' + close_restart_msg)
        print(default_dt_msg)

        if searchStatus.validStartDt is True:
            print('\nStart Date:')
            print(searchMain.startDate)

    elif searchStatus.status == 2:
        status_msg = "FINDING FILES WITHIN DATE RANGE . . ."
        os.system('cls')
        print(status_msg)
        print('\n')

    elif searchStatus.status == 3:
        status_msg = 'SEARCH FOR SOMETHING . . .'
        os.system('cls')
        print(status_msg)
        print('\n')
        print(close_restart_msg)
        print(date_rng_msg + searchMain.startDate + ' to ' +
              searchMain.endDate)
        print(search_str_msg + case_irrelevant_msg)

    elif searchStatus.status == 4:
        status_msg = 'SCANNING DOCUMENTS . . .'
        os.system('cls')
        print(status_msg)
        print(date_rng_msg + searchMain.startDate + ' to ' +
              searchMain.endDate)
        print("Searching for: ", searchMain.searchStr)
        print('\n')
        print('Total documents scanned:', searchMain.numFiles)
        print("Documents matching search criteria: ",
              len(searchMain.validDocList))
        print('Documents not matching:', searchMain.invalidDocs)
        print('\n')

    elif searchStatus.status == 5:
        status_msg = "FINISHED !"
        os.system('cls')
        print(status_msg)
        print('Total documents scanned:', searchMain.numFiles)
        print("Documents matching search criteria: ",
              len(searchMain.validDocList))
        print('Documents NOT matching:', searchMain.invalidDocs)
        print('\n')

        if len(searchMain.validDocList) == 0:
            print(no_docs_msg)
            print('\n')

            os.system('pause')
            # RESTART
            restart(searchStatus, searchMain)

        else:
            print("- - - Summary of Results - - -")
            print('Date Range: ' +
                  searchMain.startDate + ' - ' + searchMain.endDate)
            print('Searched for: ' + searchMain.searchStr + '\n')
            print("_" * 50 + "\n")
            for path, lines in searchMain.validDocList.items():
                print(path)
                for line in lines:
                    print(line)
                print('\n')

            print("_" * 50 + "\n")

        # TODO: error 8 should show here
        if searchStatus.error == 8:
            error_msg(searchStatus, searchMain)
        else:
            print("\nA log of the matching idoc's is located here: "
                  "\n'{}".format(searchStatus.log_dir))
            print("\n")

            os.system("pause")
            # RESTART
            restart(searchStatus, searchMain)


def error_msg(searchStatus, searchMain):
    '''
    Error handling - display error messages, control program flow, and clear
    bad data after error.
    '''
    if searchStatus.error == 1:
        # invalid input date
        status_output(searchStatus, searchMain)
        print('\n')

        if searchStatus.validStartDt is False:
            # start date NOT printed in status
            # print start date
            print('Start Date:')
            print(searchMain.startDate)
        elif searchStatus.validStartDt is True:
            # start date was printed in status
            # print end date too
            print('End Date:')
            print(searchMain.endDate)

        print('\n')
        print(invalidDate_msg1, seperator_msg)
        os.system("pause")

        # reuse start date?
        reuse_start(searchStatus, searchMain)

    elif searchStatus.error == 2:
        # input too short/long
        print('\n')
        status_output(searchStatus, searchMain)
        print('\n')

        if searchStatus.validStartDt is False:
            # start date NOT printed in status
            # print start date
            print('Start Date:')
            print(searchMain.startDate)
        elif searchStatus.validStartDt is True:
            # start date was printed in status
            # print end date too
            print('End Date:')
            print(searchMain.endDate)

        print('\n')
        print(date_too_short)
        print(invalidDate_msg1, seperator_msg)
        os.system("pause")

        # reuse start date?
        reuse_start(searchStatus, searchMain)

    elif searchStatus.error == 3:
        # end date is before start date
        status_output(searchStatus, searchMain)
        print('\n')

        # start date was printed in status
        # print end date too
        print('End Date:')
        print(searchMain.endDate)

        print('\n')
        print(end_b4_st_msg)
        print(invalidDate_msg1, seperator_msg)
        os.system("pause")

        # reuse start date?
        reuse_start(searchStatus, searchMain)

    elif searchStatus.error == 4:
        # date is in the future
        status_output(searchStatus, searchMain)
        print('\n')

        if searchStatus.validStartDt is False:
            # start date NOT printed in status
            # print start date
            print('Start Date:')
            print(searchMain.startDate)
        elif searchStatus.validStartDt is True:
            # start date was printed in status
            # print end date too
            print('End Date:')
            print(searchMain.endDate)

        print('\n')
        print(future_dt_msg)
        print(invalidDate_msg1, seperator_msg)
        print('\n')
        os.system("pause")

        # reuse start date?
        reuse_start(searchStatus, searchMain)

    elif searchStatus.error == 5:
        # blank input on search term
        print(blank_entry_msg)
        searchStatus.error = 0
        os.system("pause")

        main_loop(searchStatus, searchMain)

    elif searchStatus.error == 6:
        # no directories for date range
        print(no_dir_for_range)
        os.system("pause")
        # RESTART
        restart(searchStatus, searchMain)

    elif searchStatus.error == 8:
        print(log_write_error_msg)
        os.system("pause")
        # RESTART
        restart(searchStatus, searchMain)

    elif searchStatus.error == 000:
        # exiting; no error
        os.system('cls')
        response = input("Exit the program? [y/N]\n")
        if response.lower() == 'y':
            # Quit program
            os.system('cls')
            print(exit_msg)
            exit()
        elif response.lower() == 'n':
            # don't quit; RESTART
            searchStatus.error == 0
            os.system("pause")
            # RESTART
            restart(searchStatus, searchMain)
        else:
            # bad input; repeat message
            error_msg(searchStatus, searchMain)


def main_loop(searchStatus, searchMain):
    # location of the directory to be searched
    # should always be intIn
    searchStatus.search_dir = 'C:\\GENSRVNT\\IntIn\\'
    # directory log files will go after a completed search
    searchStatus.log_dir = 'C:\\GENSRVNT\\Search\\search_{}.txt'

    try:
        os.chdir(searchStatus.search_dir)
    except:
        print('The IntIn directory does not exist. '
              'Please make sure the IntIn directory is located here: {}'
              .format(searchStatus.search_dir))

    if searchStatus.validEndDt is False:
        searchMain.dateRange, searchMain.startDate, searchMain.endDate = \
            set_date_rng(searchStatus, searchMain)
        searchStatus.status = 2
        status_output(searchStatus, searchMain)

        searchMain.paths = create_paths(searchMain)
        searchMain.paths2 = find_dir(searchMain)
        import ipdb; ipdb.set_trace()  # breakpoint d452cd81 //
        if len(searchMain.paths2) == 0:
            # no files for this range
            searchStatus.error = 6
            error_msg(searchStatus, searchMain)

    searchMain.invalidDocs, searchMain.validDocList = \
        string_search(searchStatus, searchMain)

    try:
        # create and write to log file

        cur_date = datetime.datetime.today().strftime('%m-%d-%y_%I%M%S')
        with open(searchStatus.log_dir.format(cur_date), 'w+') as log_file:
            # split and format current date/time
            cur_date, cur_time = cur_date.split('_')
            cur_time = (cur_time[:2] + ':' + cur_time[2:4] + ':' +
                        cur_time[4:])

            log_file.write('Search performed ')
            log_file.write(cur_date)
            log_file.write(cur_time)
            log_file.write('\n')
            log_file.write('\n')
            log_file.write('Date Range: ')
            date_range = (searchMain.startDate + ' to ' + searchMain.endDate)
            log_file.write(date_range)
            log_file.write('\n')
            log_file.write('Searched for: ')
            log_file.write(searchMain.searchStr)
            log_file.write('\n')
            log_file.write("_" * 50 + "\n")
            log_file.write('\n')

            for path, lines in searchMain.validDocList.items():
                log_file.write(path)
                log_file.write('\n')
                for line in lines:
                    log_file.write(line)
                    log_file.write('\n')
                log_file.write('\n')
                log_file.write('\n')
    except:
        searchStatus.error = 8

    searchStatus.status = 5
    status_output(searchStatus, searchMain)


# ----- Run ----- #
searchStatus = Output()
searchMain = Search()
main_loop(searchStatus, searchMain)
