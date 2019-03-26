from datetime import datetime, date, timedelta
import pandas

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']


def format_date(date_):
    # use ifs to find seperator and create variable
    # update variable in strptime argument


    if '-' in date_:
        try:
            dateStr = datetime.strptime(date_, '%m-%d-%Y').date()
            dateStr = dateStr.strftime('%m-%d-%Y')
            return dateStr, 0
        except:
            try:
                dateStr = datetime.strptime(date_, '%m-%d-%y').date()
                dateStr = dateStr.strftime('%m-%d-%Y')
                return dateStr, 0
            except:
                return date_, 1

    elif '.' in date_:
        try:
            dateStr = datetime.strptime(date_, '%m.%d.%Y').date()
            dateStr = dateStr.strftime('%m-%d-%Y')
            return dateStr, 0
        except:
            try:
                dateStr = datetime.strptime(date_, '%m.%d.%y').date()
                dateStr = dateStr.strftime('%m-%d-%Y')
                return dateStr, 0
            except:
                return date_, 1

    elif '/' in date_:
        try:
            dateStr = datetime.strptime(date_, '%m/%d/%Y').date()
            dateStr = dateStr.strftime('%m-%d-%Y')
            return dateStr, 0
        except:
            try:
                dateStr = datetime.strptime(date_, '%m/%d/%y').date()
                dateStr = dateStr.strftime('%m-%d-%Y')
                return dateStr, 0
            except:
                return date_, 1

    elif '\\' in date_:
        try:
            dateStr = datetime.strptime(date_, '%m\\%d\\%Y').date()
            dateStr = dateStr.strftime('%m-%d-%Y')
            return dateStr, 0
        except:
            try:
                dateStr = datetime.strptime(date_, '%m\\%d\\%y').date()
                dateStr = dateStr.strftime('%m-%d-%Y')
                return dateStr, 0
            except:
                return date_, 1
    else:
        try:
            dateStr = datetime.strptime(date_, '%m%d%Y').date()
            dateStr = dateStr.strftime('%m-%d-%Y')
            return dateStr, 0
        except:
            try:
                dateStr = datetime.strptime(date_, '%m%d%y').date()
                dateStr = dateStr.strftime('%m-%d-%y')
                return dateStr, 0
            except:
                return date_, 1


def vali_date_rng(start, end=None):
    '''
    Takes a start date, or start and end date as a string formated as m-d-yyyy
    Ensure dates are valid for creating a historical date range by:
    Checking that date is not in the future
    Checking that start date is before end

    Return an error code
    - 0 meaning date(s) are valid
    - 1 meaning start date is invalid
    - 2 meaning end date is invalid
    - 3 menaing start date is later than end date

    ***MUST USE: from datetime import datetime, date
    '''

    from datetime import datetime, date

    start = datetime.strptime(start, '%m-%d-%Y').date()

    if end is None:
        # check start date only
        if start > date.today():
            # date is in the future
            return 4
        else:
            # make sure date is not more than 5yrs old
            if start < (date.today() - timedelta(days=(365 * 5))):
                return 7
            return 0
    else:
        end = datetime.strptime(end, '%m-%d-%Y').date()
        # check end date
        if end > date.today():
            # end date is in the future
            return 2
        elif start > end:
            return 3
        else:
            # make sure date is not more than 5yrs old
            if end < (date.today() - timedelta(days=(365 * 5))):
                return 7
            return 0


def set_date_rng(dateRange: list):
    '''
    Control input and verification of a date range.
    Able to reuse a start date if it was entered correctly,
    followed by a bad end date.
    Will return:
    error,
    startDate,
    endDate,
    dateRange,
    '''
    error = 0
    validEndDt = False
    # dateRange = {'start': None, 'end':None}
    endDate = ''

    while dateRange[0] is None:
        # set and print default date
        # defaultStart = date.today() - timedelta(1)
        defaultStart = date.today() - timedelta(1)
        defaultStart = defaultStart.strftime('%m-%d-%Y')
        print('[{}]'.format(defaultStart))

        # Take input for start date
        startDate = input("Start Date: ") or defaultStart

        if startDate.lower() == "exit":
            error = 999
            return error, dateRange, startDate, endDate
        elif startDate.lower() == "date":
            # restart code
            error = 111
            return error, dateRange, startDate, endDate
        # rough length check
        elif len(startDate) > 10 or len(startDate) < 6:
            # input date too short or too long
            error = 2
            return error, dateRange, startDate, endDate
        else:
            # reformat date
            startDate, error = format_date(startDate)
            if error != 0:
                return error, dateRange, startDate, endDate

            # print formated date
            stMonth, stDay, stYear = startDate.split('-')
            print(months[int(stMonth) - 1], stDay + ',', stYear + '\n')

            # check for error
            if error != 0:
                return error, dateRange, startDate, endDate

            # make sure date is valid
            error = vali_date_rng(startDate)
            # check for error
            if error != 0:
                return error, dateRange, startDate, endDate
            else:
                dateRange = [startDate, None]

    startDate = dateRange[0]

    while dateRange[1] is None:
        # set and print default date
        defaultEnd = date.today().strftime('%m-%d-%Y')
        print('\n')
        print('[{}]'.format(defaultEnd))

        # Take input for end date
        endDate = input("End Date: ") or defaultEnd

        if endDate.lower() == "exit":
            error = 999
            return error, dateRange, startDate, endDate
        elif endDate.lower() == "date":
            # restart code
            error = 111
            return error, dateRange, startDate, endDate
        # rough length check
        elif len(endDate) > 10 or len(endDate) < 6:
            # input date too short
            error = 2
            return error, dateRange, startDate, endDate
        else:
            # find separator; reformat date; make sure date is valid
            endDate, error = format_date(endDate)
            if error != 0:
                return error, dateRange, startDate, endDate

            # print formated date
            endMonth, endDay, endYear = endDate.split('-')
            print(months[int(endMonth) - 1], endDay + ',', endYear + '\n')

            # check for error
            if error != 0:
                return error, dateRange, startDate, endDate

            error = vali_date_rng(startDate, endDate)
            # check for error
            if error != 0:
                return error, dateRange, startDate, endDate
            else:
                dateRange = [startDate, endDate]
                return error, dateRange, startDate, endDate
