import pandas as pd


# Input: csvFileName - String of csv file name
# Output: Returns csv file
def readCsv(csvFileName):
    df = pd.read_csv(csvFileName)
    return df


def readTwoColumnOfCsvFromRowXToRowY(csvFile, firstColumnName, secondColumnName, start, end):
    fullList = csvFile[[firstColumnName, secondColumnName]]
    return fullList.iloc[start:end]


# Input: csvFile - String of csv file to read
#        columnName - String of column to read
#        noOfRows - Integer of rows to read (default is 0)
# Output: Return a column of csv file
def readCsvByColumnName(csvFile, columnName, noOfRows=0):
    if noOfRows == 0:
        return csvFile[columnName]
    else:
        return csvFile[columnName][0:noOfRows]


# Input: csvFile - String of csv file to read
#        noOfRows - Integer of rows to read (default is 0)
# Output: Return rows of csv file (default is 0. Example: 2 returns first two rows)
def readCsvByRow(csvFile, noOfRows=0):
    if noOfRows == 0:
        return csvFile
    else:
        return csvFile.head(noOfRows)


# Input: csvFile - String of csv file to read
#        start - Start position to read from
#        end - Last position to read until (includes this row)
# Output: Return rows of csv file
def readCsvFromRowXToRowY(csvFile, start, end):
    return csvFile.iloc[start:end]


# Input: csvFile - String of csv file to read
#        columnName - String name of column to read
#        start - Start position to read from
#        end - Last position to read until (includes this row)
# Output: Return rows of csv file
def readCsvOfAColumnFromRowXToRowY(csvFile,columnName , start, end):
    if end == ':':
        return csvFile[columnName].iloc[start:]
    return csvFile[columnName].iloc[start:end]


# Input: csvFile - String of csv file to read
#        csvColumn - String of csvColumn to read
# Output: Return int value of column of cell with the highest value (E,g return 650 if it is highest in any cell in a column)
def getMaxValueOfAColumn(csvFile, csvColumn):
    maxValue = csvFile[csvColumn].max()
    return maxValue

