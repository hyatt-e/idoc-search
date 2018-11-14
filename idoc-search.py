#! G:\WPy-3661\python\ENV\idoc-search\Scripts\activate.bat

import datetime
import os
import re
from datetime import timedelta

import pandas

# GLOBAL VARIABLES #
doctype = None
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']


#   #   #   #   #   #   #   #   #


class Output:
	search_dir = ''
	log_dir = ''

	error = 0
	status = ''
	exit = False
	errorCnt = 0
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


def future_date_chk(inDate):
	if inDate > datetime.date.today().strftime('%m-%d-%Y'):
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
		month = searchMain.startDate[:2]
		day = searchMain.startDate[2:4]
		year = searchMain.startDate[4:]
	else:
		month, day, year = date.split(separator)

	if len(month) == 1:
		month = '0' + month
	if len(day) == 1:
		day = '0' + day
	if len(year) == 2:
		# if year is greater than current year, assume it's a 20th cent. year
		if year > datetime.datetime.today().strftime('%Y'):
			year = '19' + year
		else:
			year = '20' + year
	# else:
	# 	# invalid date
	# 	searchStatus.error = 1
	# 	error_msg(searchStatus, searchMain)

	# replace separators with '-'
	date = month + '-' + day + '-' + year
	return date


def vali_date(searchMain, searchStatus):
	start = searchMain.startDate
	end = searchMain.endDate

	if end == '':
		searchStatus.error = future_date_chk(start)
		if searchStatus.error != 0:
			error_msg(searchStatus, searchMain)

		stMonth, stDay, stYear = start.split('-')
		print(months[int(stMonth) - 1], stDay + ',', stYear + '\n')
		startDate = stMonth + '-' + stDay + '-' + stYear
		return startDate
	elif end != '':
		searchStatus.error = future_date_chk(start)
		if searchStatus.error != 0:
			error_msg(searchStatus, searchMain)

		searchStatus.error = start_end_chk(start, end)
		if searchStatus.error != 0:
			error_msg(searchStatus, searchMain)

		endMonth, endDay, endYear = end.split('-')
		print(months[int(endMonth) - 1], endDay + ',', endYear + '\n')
		endDate = endMonth + '-' + endDay + '-' + endYear
		# os.system("pause")
		return endDate


def set_time_rng(searchStatus, searchMain):
	# print status; print errors, if any
	searchStatus.error = 0
	searchStatus.status = "SELECT DATE RANGE . . ."
	searchStatus.exit = False
	status_output(searchStatus, searchMain)
	# error_msg(searchStatus, searchMain)

	while searchStatus.exit == False:
		if searchStatus.validStartDt == False:
			# set and print default date
			defaultStart = datetime.date.today() - timedelta(1)
			defaultStart = defaultStart.strftime('%m-%d-%Y')
			print('\n')
			print('[{}]'.format(defaultStart))

			# Take input for start date
			searchMain.startDate = input("Start Date: ") or defaultStart

			if searchMain.startDate.lower() == "exit":
				searchStatus.exit = True
				searchStatus.error = 11
				error_msg(searchStatus, searchMain)
			elif len(searchMain.startDate) < 4:
				# input date too short
				searchStatus.error = 2
				searchMain.startDate = ''
				error_msg(searchStatus, searchMain)
			# check for single digit numbers and add 0's
			else:
				# find separator; reformat date; make sure date is valid
				if '\\' in searchMain.startDate:
					separator = '\\'
					# convert any single digit numbers; make all separators -
					searchMain.startDate = format_date(searchMain.startDate, separator)
					searchMain.startDate = vali_date(searchMain, searchStatus)
					searchStatus.validStartDt = True
				elif '/' in searchMain.startDate:
					separator = '/'
					# convert any single digit numbers; make all separators -
					searchMain.startDate = format_date(searchMain.startDate, separator)
					searchMain.startDate = vali_date(searchMain, searchStatus)
					searchStatus.validStartDt = True
				elif '-' in searchMain.startDate:
					separator = '-'
					# convert any single digit numbers; make all separators -
					searchMain.startDate = format_date(searchMain.startDate, separator)
					searchMain.startDate = vali_date(searchMain, searchStatus)
					searchStatus.validStartDt = True
				elif '.' in searchMain.startDate:
					separator = '.'
					# convert any single digit numbers; make all separators -
					searchMain.startDate = format_date(searchMain.startDate, separator)
					searchMain.startDate = vali_date(searchMain, searchStatus)
					searchStatus.validStartDt = True
				else:
					separator = ''
					# convert any single digit numbers; make all separators -
					searchMain.startDate = format_date(searchMain.startDate, separator)

					if (re.findall("((\d{1,2})(\d{1,2})(\d{4}))", searchMain.startDate)) != []:
						match = re.findall("((\d{1,2})(\d{1,2})(\d{4}))", searchMain.startDate)
					else:
						# invalid date
						searchStatus.error = 1
						searchMain.startDate = ''
						error_msg(searchStatus, searchMain)
					searchMain.startDate = vali_date(searchMain, searchStatus)
					searchStatus.validStartDt = True

		elif searchStatus.validEndDt == False:
			status_output(searchStatus, searchMain)

			# set and print default date
			defaultEnd = datetime.date.today().strftime('%m-%d-%Y')
			print('\n')
			print('[{}]'.format(defaultEnd))

			# Take input for end date
			searchMain.endDate = input("End Date: ") or defaultEnd

			if searchMain.endDate.lower() == "exit":
				searchStatus.exit = True
				searchStatus.error = 11
				error_msg(searchStatus, searchMain)
			elif len(searchMain.endDate) < 4:
				# input date too short
				searchStatus.error = 2
				searchMain.endDate = ''
				error_msg(searchStatus, searchMain)

			# check for single digit numbers and add 0's
			else:
				# find separator; reformat date; make sure date is valid
				if '\\' in searchMain.endDate:
					separator = '\\'
					# convert any single digit numbers; make all separators -
					searchMain.endDate = format_date(searchMain.endDate, separator)
					searchMain.endDate = vali_date(searchMain, searchStatus)
					searchStatus.validEndDt = True
				elif '/' in searchMain.endDate:
					separator = '/'
					# convert any single digit numbers; make all separators -
					searchMain.endDate = format_date(searchMain.endDate, separator)
					searchMain.endDate = vali_date(searchMain, searchStatus)
					searchStatus.validEndDt = True
				elif '-' in searchMain.endDate:
					separator = '-'
					# convert any single digit numbers; make all separators -
					searchMain.endDate = format_date(searchMain.endDate, separator)
					searchMain.endDate = vali_date(searchMain, searchStatus)
					searchStatus.validEndDt = True
				elif '.' in searchMain.endDate:
					separator = '.'
					# convert any single digit numbers; make all separators -
					searchMain.endDate = format_date(searchMain.endDate, separator)
					searchMain.endDate = vali_date(searchMain, searchStatus)
					searchStatus.validEndDt = True
				else:
					separator = ''
					# convert any single digit numbers; make all separators -
					searchMain.endDate = format_date(searchMain.endDate, separator)

					if (re.findall("((\d{1,2})(\d{1,2})(\d{4}))", searchMain.endDate)) != []:
						match = re.findall("((\d{1,2})(\d{1,2})(\d{4}))", searchMain.endDate)
					else:
						# invalid date
						searchStatus.error = 1
						searchMain.endDate = ''
						error_msg(searchStatus, searchMain)
					searchMain.endDate = vali_date(searchMain, searchStatus)
					searchStatus.validEndDt = True

		if searchStatus.error != 0:
			if searchStatus.errorCnt >= 5:
				print(tooManyErrors_msg10)
				error_msg(searchStatus, searchMain)
			else:
				searchStatus.errorCnt += 1
				error_msg(searchStatus, searchMain)
		elif searchStatus.validEndDt == True:
			searchStatus.exit = True

	searchMain.dateRange = pandas.date_range(start=searchMain.startDate, end=searchMain.endDate)
	searchMain.dateRange = pandas.Series(searchMain.dateRange.format())

	return searchMain.dateRange, searchMain.startDate, searchMain.endDate


def create_paths(searchMain):
	paths = []
	for date in searchMain.dateRange:
		year, month, day = date.split('-')
		paths.append('G:\\WPy-3661\\python\\USF-997\\IntIn-DEV\\#{}\\{}\\{}\\'.format(year, month, day))
	return paths


def find_dir(searchMain):
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
		if good_path == True:
			dirs = os.listdir()
			for dirty in dirs:
				paths2.append(path + dirty + '\\')
	return paths2


def string_search(searchStatus, searchMain):
	searchStatus.status = "SEARCH FOR STRING . . ."
	status_output(searchStatus, searchMain)

	searchMain.searchStr = input('').lower()
	if searchMain.searchStr.lower() == "exit":
		searchStatus.exit = True
		searchStatus.error = 11
		error_msg(searchStatus, searchMain)
	elif searchMain.searchStr == '':
		searchStatus.error = 5
		error_msg(searchStatus, searchMain)

	searchStatus.status = "SCANNING DOCUMENTS . . ."
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

	# Search each line for string. If line is found to contain the string, add line and file to log
	line_num = 0
	for line in lines:
		line_num += 1
		if searchMain.searchStr in line:
			matching_lines.append("Line " + str(line_num) + ": " + line)
			continue

	return matching_lines


# ______________________________________________________________________________________________________________________#
instruction_msg1 = "Please enter dates with the month, followed by day, followed by year\n. - \\ / or no separators may be used\nEnter 'exit' to close the program\n"
instruction_msg2 = "Press 'Enter' to use the [Default Date]"
instruction_msg3 = "This is not case sensitive (capital letters will be lower-cased).\nEnter 'exit' to close the program\n"
file_not_found_msg = "Could not open the US Foods Control Numbers document!\nMake sure the file is in the correct location:\n'G:\\WPy-3661\\python\\USF-997\\US Foods Control Numbers.csv'"
no_dir_for_range = "No directories were found matching this date range.\nThere may be no inbound files for the specified dates."
invalidDate_msg1 = "Please enter a valid date.\n"
invalidDate_msg2 = "Dates may use . - \\ / or no separators may be used to separate month, day, and year.\nIf using no separators, enter an 8 digit string (ie. March 9, 1994 as 03091994)"
date_too_short = "Your entry does not contain enough characters to be a date.\n"
invalidDate_msg3 = "The End Date must be later than the Start Date.\n"
invalidDate_msg4 = "You cannot select a date that is in the future.\n"
invalidDate_msg5 = "Your entry was blank.\n"
tooManyErrors_msg10 = "Are you sure you're entering a date?"
exit_msg = "BYE."


# ______________________________________________________________________________________________________________________#

def status_output(searchStatus, searchMain):
	# control output
	# display info and instructions through out program
	if searchStatus.status == "SELECT DATE RANGE . . .":
		os.system('cls')
		print(searchStatus.status)
		print('\n')
		print(instruction_msg1)
		print(instruction_msg2)

		if searchStatus.validStartDt == True:
			print('\nStart Date:')
			print(searchMain.startDate)

	elif searchStatus.status == 'FINDING FILES WITHIN DATE RANGE . . .':
		os.system('cls')
		print(searchStatus.status)
		print('\n')

	elif searchStatus.status == 'SEARCH FOR STRING . . .':
		os.system('cls')
		print(searchStatus.status)
		print('\n')
		print(instruction_msg3)
		print("Date Range: ", searchMain.startDate + ' - ' + searchMain.endDate)
		print("Documents within the date range shown above will be searched for the following:\n")

	elif searchStatus.status == 'SCANNING DOCUMENTS . . .':
		os.system('cls')
		print(searchStatus.status)
		print("Date Range: ", searchMain.startDate + ' - ' + searchMain.endDate)
		print("Searching for: ", searchMain.searchStr)
		print('\n')
		print('Total documents scanned:', searchMain.numFiles)
		print("Documents matching search criteria: ", len(searchMain.validDocList))
		print('Documents not matching:', searchMain.invalidDocs)
		print('\n')

	elif searchStatus.status == "FINISHED !":
		os.system('cls')
		print(searchStatus.status)
		print('Total documents scanned:', searchMain.numFiles)
		print("Documents matching search criteria: ", len(searchMain.validDocList))
		print('Documents not matching:', searchMain.invalidDocs)
		print('\n')

		if len(searchMain.validDocList) == 0:
			print("No idoc's containing the search criteria found in this date range")
			print("Would you like to try again?")
			print("Enter 'S' to perform a different search within the same date range.")
			print("Enter 'D' to change the date range.")
			print("Enter 'EXIT' to close.")
			restart = input('')
			if restart.lower() == 's':
				searchStatus.error = 0
				main_loop(searchStatus, searchMain)
			elif restart.lower() == 'd':
				searchStatus.error = 0
				searchStatus.validStartDt = False
				searchStatus.validEndDt = False
				main_loop(searchStatus, searchMain)
			elif restart.lower() == 'exit':
				print(exit_msg)
				quit()
			else:
				searchStatus.status = "FINISHED !"
				status_output(searchStatus, searchMain)
		else:
			print("- - - Summary of Results - - -")
			print('Date Range: ' + searchMain.startDate + ' - ' + searchMain.endDate)
			print('Searched for: ' + searchMain.searchStr + '\n')
			print("_" * 50 + "\n")
			for path, lines in searchMain.validDocList.items():
				print(path)
				for line in lines:
					print(line)
				print('\n')

			print("_" * 50 + "\n")

		print("\nA log of the matching idoc's is located here: '{}".format(searchStatus.log_dir))
		print("\n")
		print("Would you like to do another search?")
		print("Enter 'S' to perform a different search within the same date range.")
		print("Enter 'D' to change the date range.")
		print("Enter 'EXIT' to close.")
		restart = input('')
		if restart.lower() == 's':
			searchStatus.error = 0
			main_loop(searchStatus, searchMain)
		elif restart.lower() == 'd':
			searchStatus.error = 0
			searchStatus.validStartDt = False
			searchStatus.validEndDt = False
			main_loop(searchStatus, searchMain)
		elif restart.lower() == 'exit':
			print(exit_msg)
			quit()
		else:
			searchStatus.status = "FINISHED !"
			status_output(searchStatus, searchMain)


def error_msg(searchStatus, searchMain):
	# error handling - display error messages for specific situations
	if searchStatus.error == 1:
		# invalid input date
		status_output(searchStatus, searchMain)
		print(invalidDate_msg1, invalidDate_msg2)
		os.system("pause")
		searchStatus.error = 0
		main_loop(searchStatus, searchMain)

	elif searchStatus.error == 2:
		# input too short
		status_output(searchStatus, searchMain)
		print(date_too_short, invalidDate_msg1, invalidDate_msg2)
		os.system("pause")
		searchStatus.error = 0
		main_loop(searchStatus, searchMain)

	elif searchStatus.error == 3:
		# end date is before start date
		status_output(searchStatus, searchMain)
		print('\n')
		print(invalidDate_msg1, invalidDate_msg2)
		print('\n')
		print(invalidDate_msg3)

		# reuse start date?
		if searchStatus.validStartDt == True:
			print('\nStart Date:')
			print(searchMain.startDate)
			response = input('Would you like to use this start date? [y/N]\n')

			if response.lower() == 'n':
				searchStatus.validStartDt = False

		searchStatus.error = 0
		main_loop(searchStatus, searchMain)

	elif searchStatus.error == 4:
		# date is in the future
		status_output(searchStatus, searchMain)
		print(invalidDate_msg1, invalidDate_msg2)
		print('\n')
		print(invalidDate_msg4)
		os.system("pause")
		searchStatus.error = 0  # reuse start date?
		if searchStatus.validStartDt == True:
			print('\nStart Date:')
			print(searchMain.startDate)
			print("Would you like to try again?")
			print("Enter 'S' to perform a different search within the same date range.")
			print("Enter 'D' to change the date range.")
			print("Enter 'EXIT' to close.")
			restart = input('')
			if restart.lower() == 's':
				searchStatus.error = 0
				main_loop(searchStatus, searchMain)
			elif restart.lower() == 'd':
				searchStatus.error = 0
				searchStatus.validStartDt = False
				searchStatus.validEndDt = False
				main_loop(searchStatus, searchMain)
			elif restart.lower() == 'exit':
				print(exit_msg)
				quit()
			else:
				searchStatus.status = "FINISHED !"
				status_output(searchStatus, searchMain)
		else:
			main_loop(searchStatus, searchMain)

	elif searchStatus.error == 5:
		# blank input
		print(invalidDate_msg5, invalidDate_msg1, invalidDate_msg2)
		searchStatus.error = 0
		os.system("pause")
		# check where the error occurred
		if searchStatus.validStartDt == True and searchStatus.validEndDt == True:
			# if there are valid dates, the error occurred on the search string input
			main_loop(searchStatus, searchMain)
		else:
			# error was on date input
			main_loop(searchStatus, searchMain)

	elif searchStatus.error == 6:
		# no applicable files found
		print(no_dir_for_range)
		print("Would you like to try again?")
		print("Enter 'S' to perform a different search within the same date range.")
		print("Enter 'D' to change the date range.")
		print("Enter 'EXIT' to close.")
		restart = input('')
		if restart.lower() == 's':
			searchStatus.error = 0
			main_loop(searchStatus, searchMain)
		elif restart.lower() == 'd':
			searchStatus.error = 0
			searchStatus.validStartDt = False
			searchStatus.validEndDt = False
			main_loop(searchStatus, searchMain)
		elif restart.lower() == 'exit':
			print(exit_msg)
			quit()
		else:
			searchStatus.status = "FINISHED !"
			status_output(searchStatus, searchMain)

	elif searchStatus.error == 8:
		print('\nThere was an error while writing the log file.')
		print("Would you like to try again?")
		print("Enter 'S' to perform a different search within the same date range.")
		print("Enter 'D' to change the date range.")
		print("Enter 'EXIT' to close.")
		restart = input('')
		if restart.lower() == 's':
			searchStatus.error = 0
			main_loop(searchStatus, searchMain)
		elif restart.lower() == 'd':
			searchStatus.error = 0
			searchStatus.validStartDt = False
			searchStatus.validEndDt = False
			main_loop(searchStatus, searchMain)
		elif restart.lower() == 'exit':
			print(exit_msg)
			quit()
		else:
			searchStatus.status = "FINISHED !"
			status_output(searchStatus, searchMain)

	elif searchStatus.error == 10:
		# more than 5 errors
		status_output(searchStatus, searchMain)
		print(invalidDate_msg1, invalidDate_msg2)
		print('\n')
		print(tooManyErrors_msg10)
		os.system("pause")
		searchStatus.error = 0
		main_loop(searchStatus, searchMain)

	elif searchStatus.error == 11:
		# exiting; no error
		print(exit_msg)
		os.system("pause")
		quit()


def main_loop(searchStatus, searchMain):
	# location of the directory to be searched
	# should always be intIn
	searchStatus.search_dir = 'G:\\WPy-3661\\python\\USF-997\\IntIn-DEV\\'
	# directory log files will go after a completed search
	searchStatus.log_dir = 'G:\\WPy-3661\\python\\idoc-search\\Logs\\search_{}.txt'

	os.chdir(searchStatus.search_dir)
	if searchStatus.validEndDt == False:
		searchMain.dateRange, searchMain.startDate, searchMain.endDate = set_time_rng(searchStatus, searchMain)
		searchStatus.status = 'FINDING FILES WITHIN DATE RANGE . . .'
		status_output(searchStatus, searchMain)

		searchMain.paths = create_paths(searchMain)
		searchMain.paths2 = find_dir(searchMain)
		if len(searchMain.paths2) == 0:
			# no files for this range
			searchStatus.error = 6
			error_msg(searchStatus, searchMain)

	searchMain.invalidDocs, searchMain.validDocList = string_search(searchStatus, searchMain)

	try:
		cur_date = datetime.datetime.today().strftime('%m-%d-%y_%I%M%S')
		with open(searchStatus.log_dir.format(cur_date), 'w+') as log_file:
			log_file.write('Date Range: ' + searchMain.dateRange + '\n')
			log_file.write('Searched for:' + searchMain.searchStr + '\n' + '\n')

			for path, lines in searchMain.validDocList.items():
				log_file.write(str(path) + '\n')
				for line in lines:
					print(line)
				print('\n')
	except:
		searchStatus.error = 8

	searchStatus.status = "FINISHED !"
	status_output(searchStatus, searchMain)


# ----- Run ----- #
searchStatus = Output()
searchMain = Search()
main_loop(searchStatus, searchMain)
