import os
import pandas


def last_accepted(control_num_file_path):
    '''
    Get the control numbers from 'US Foods Control Numbers.xlsx'
    Return the last855 and last 810 conrol number
    '''
    usf_ctrl_nums = ''
    last810 = 0
    last855 = 0
    error = 0

    try:
        usf_ctrl_nums = \
            pandas.read_excel(control_num_file_path, header=None)
    except:
        # issue loading file to python
        # usually file not found or wrong format
        error = 5
        return error, usf_ctrl_nums, last810, last855

    docType = usf_ctrl_nums.iloc[0, 0]
    if docType == "810's":
        last810 = int(usf_ctrl_nums.iloc[0, 1])
    else:
        error = 6
        return error, usf_ctrl_nums, last810, last855

    docType = usf_ctrl_nums.iloc[2, 0]
    if docType == "855's":
        last855 = int(usf_ctrl_nums.iloc[2, 1])
    else:
        error = 6
        return error, usf_ctrl_nums, last810, last855

    return error, usf_ctrl_nums, last810, last855


def split_segs(file_path):
    '''
    Takes file path as text string.
    Splits doc by line, then by segment.
    Returns dict with first segments of line as key, and a list of each segment
    of the line as the value.
    '''
    segments = {}

    file = open(file_path)
    file = file.read()

    # split line apart
    lines = file.split("~")

    for lineNum, strng in enumerate(lines):
        # split line into fields
        fields = strng.split('^')

        # get rid of extra white space
        for fieldNum, x in enumerate(fields):
            x = x.replace('  ', '')
            fields[fieldNum] = x

        segments[lineNum] = fields

    return segments


def create_paths(dateRange: tuple, search_dir: str) -> (int, list):
    '''
    Use a series of dates to create file paths for Gentran IntIn directory
    '''
    date_paths = []
    part_paths = []
    paths = []
    error = 0

    dateRange = pandas.date_range(start=dateRange[0], end=dateRange[1])
    dateRange = pandas.Series(dateRange.format())

    # find all directories associated with date range
    for date_ in dateRange:
        year, month, day = date_.split('-')
        date_paths.append(search_dir + '#{}\\{}\\{}\\'
                          .format(year, month, day))

    # check that paths are valid
    # find file names and add to path
    for path in date_paths:
        # check that the path is valid
        try:
            os.chdir(path)
            # path exists
            good_path = True
        except FileNotFoundError:
            # paths.remove(path)
            good_path = False

        # if the path exists, get all directories within it
        # these directories are broken down by hour
        if good_path is True:
            dirs = os.listdir()
            for directory in dirs:
                part_paths.append(path + directory + '\\')

    # find all files in directories
    for path in part_paths:
        for file in os.listdir(path):
            # Search all dirs within these paths
            docPath = path + file
            try:
                file = open(docPath)
                paths.append(docPath)
            except:
                # something wrong with the file
                error = 1
                continue

    return error, paths


def check_sort_file(paths: list) -> (list, list, dict, dict, int):
    '''
    Check for doc type and partner num.
    File will be split by segment and checked again if the partner number
    and document type are somewhere in the documnet.
    INPUT: paths
    '''
    segments810 = {}
    segments855 = {}
    valid810 = []
    valid855 = []
    invalidDocs = 0

    # global segmentFiles -> searchData.segmentFiles
    # global numFiles -> searchData.numFiles
    # global validDocList -> searchData.validDocList
    # global validDoc -> ?
    # global invalidDocs -> searchData.invalidDocs

    for path in paths:

        file = open(path)
        file = file.read()

        # rough check for doc type and partner number
        if '997' and '621418185' in file:
            # check that doc type and partner number are in correct places
            segments = split_segs(path)

            partner = (segments[0])[6]
            idoc = (segments[2])[1]
            docType = int((segments[4])[1])

            if partner == '621418185':
                if idoc == "997":
                    if docType == 810:
                        valid810.append(path)
                        segments810[path] = segments
                    elif docType == 855:
                        valid855.append(path)
                        segments855[path] = segments
                    else:
                        invalidDocs += 1
                else:
                    invalidDocs += 1
            else:
                invalidDocs += 1
        else:
            invalidDocs += 1

    return valid810, valid855, segments810, segments855, invalidDocs


def find_rejects(files: dict) -> (list, dict, dict):
    '''
        Find any errors in the documents listed in validDocList.
       Specifically, check the AK2 and AK5 segments; capture the control
       numbers listed here and use in output
    '''

    unknownDocs = {}
    acceptedDocs = []
    rejectedDocs = {}
    linesAK = []
    filesAK = []

    # AK2 segment found in file
    # the following lines until AK9 will all need to be stored
    ak2_flag = False

    for path, file in files.items():
        # list the file path before segments
        filesAK.append(path)
        linesAK = []
        ak2_flag = False

        for key, line in file.items():
            if 'AK2' in line:
                # if ak2_flag=True, this is a new ctrl number
                if ak2_flag is True:
                    # append to list and start new aksegments list
                    filesAK.append(linesAK)
                    linesAK = line
                else:
                    # first AK2 field in file
                    ak2_flag = True
                    linesAK = line

            # check for AK9; marks end of AK segments; done with this file
            elif 'AK9' in line:
                filesAK.append(linesAK)

                # stop loop; don't need anything else from file
                break

            # check ak2_flag
            elif ak2_flag is True:
                # this segment is after an Ak2, but before AK9
                # need to keep this segment

                linesAK += line

            else:
                # ak2_flag is false so haven't reached AK segments yet
                continue

    # AK segments found;
    # Make list of control numbers for Rejected Docs (AK5^R) and
    # Accepted Docs (AK5^A)
    for line in filesAK:
        print(line) # print for debug
        if isinstance(line, str) is True:
            # this is the file path/name
            docPath = line
        # elif len(line[4]) == 1:
            # assume this is the accepted/rejected field
        elif line[4] == 'A':
            acceptedDocs.append(int(line[2]))
        elif 'R' in line:
            import ipdb; ipdb.set_trace()
            rejectedDocs[docPath] = line[2]
        else:
            unknownDocs[docPath] = line[2]

    return acceptedDocs, rejectedDocs, unknownDocs


def new_ctrl_nums(acceptedDocs: list, rejectedDocs: dict,
                  lastCtrlNum: int) -> int:
    '''
    Use list of accepted ctrl nums to update the xlsx file.
    Don't update if there are any rejected documents.
    Return -> new control nums if successful; None if not.
    '''

    newCtrls = []
    # only update when no rejects were found
    assert len(rejectedDocs) == 0, \
        "Rejected Documents were found while updating control numbers"
    assert len(acceptedDocs) > 0, \
        "No accepted documents found while updating control numbers"

    # find lastCtrlNum in acceptedDocs
    sorted(acceptedDocs)
    i = [i for i, x in enumerate(acceptedDocs) if x == lastCtrlNum]

    # i should be have one or no values
    assert len(i) <= 1, \
        ("The last ctrl num ({}) was found multiple times in the list of newly accepted documents: {}"
            .format(lastCtrlNum, acceptedDocs))

    # if len(i) is 0:
    #     # add lastCtrlNum and sort list
    #     acceptedDocs.append(lastCtrlNum)
    #     acceptedDocs = sorted(acceptedDocs)
    # else:
    #     for doc in acceptedDocs:
    #         if doc <= lastCtrlNum:
    #             acceptedDocs.remove(doc)
    #     acceptedDocs = sorted(acceptedDocs)

    # seperate new ctrl nums from old
    for ctrl in acceptedDocs:
        if ctrl >= lastCtrlNum:
            newCtrls.append(ctrl)
        else:
            pass

    if len(newCtrls) == 0:
        return None
    else:
        return newCtrls


def continuous_ctrls(newCtrls, lastCtrl):
    '''
    Check that all there are no missing numbers, starting at the last control
    number recorded in the excel sheet (arg: lastCtrl) and going through the
    list of new control nums (arg: newCtrls).
    Return: newCtrls: lst, error: int
    Return None for list if there's an error.
    '''

    allCtrls = newCtrls
    allCtrls.append(lastCtrl)
    allCtrls = sorted(allCtrls)

    # check continuity
    if len(newCtrls) > 0:
        if all(a + 1 == b for a, b in
               zip(allCtrls, allCtrls[1:])):
            # Don't need the lastCtrlNum at beginning of list
            return newCtrls, 0
        else:
            # non continuous list
            return None, 10
    else:
        # no new ctrl nums
        return None, 8


def write_to_file(newestCtrlNum, filePath, docType):
    error = 0
    # check for file and create DataFrame
    try:
        ctrlNums = \
            pandas.read_excel(filePath, header=None)
    except:
        # issue loading file to python
        # usually file not found or wrong format
        error = 5

    # update DataFrame
    # 810
    if docType == 810:
        ctrlNums.iloc[0, 1] = newestCtrlNum
    # 855
    elif docType == 855:
        ctrlNums.iloc[2, 1] = newestCtrlNum

    # write to the file
    writer = pandas.ExcelWriter(filePath)
    ctrlNums.to_excel(writer, 'Sheet1', header=False, index=False)
    writer.save()

    return error
