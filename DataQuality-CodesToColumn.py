'''

California State Water Resources Control Board (SWRCB)
Office of Information Management and Analysis (OIMA) 

Michelle Tang
https://github.com/mmtang

---

This script processes output files from the 'CEDEN_to_DataCaGov/CEDEN_DataRefresh.py" script: 
https://github.com/CAWaterBoardDataCenter/CEDEN_to_DataCAGov-1. It separates the concatenated QA, 
Batch Verification, ResQual, and other codes listed in the 'DataQualityIndicator' field and copies 
them to a new file ('new-file.csv') as individual records. The new file contains all of the original 
data with the addition of two new fields:

(1) 'DataQualityIndicatorType'  = the code category (BatchVerification, Datum, QACode, ResultQualCode)
(2) 'DataQualityIndicatorCode'  = the actual code (e.g. NR, VBY, VLC)

The two fields listed above are used by OIMA staff to produce a summary of the data quality indicator 
codes associated with each indicator type and data quality category. The output of this script should
not be used for any other purpose. 

Requirements: Python 3.X

'''

import re

dataFile = "WaterChemistryData.csv"
targetName = "new-file.csv"
targetFile = open(targetName, "w")

indicators = ["BatchVerification", "Datum", "Latitude", "QACode", "ResultQualCode"]

print("Writing: " + targetName)
print("Please wait...")

# new header
header = "Program|ParentProject|Project|StationName|StationCode|SampleDate|CollectionTime|LocationCode|CollectionDepth|UnitCollectionDepth|SampleTypeCode|CollectionReplicate|ResultsReplicate|LabBatch|LabSampleID|MatrixName|MethodName|Analyte|Unit|Result|Observation|MDL|RL|ResultQualCode|QACode|BatchVerification|ComplianceCode|SampleComments|CollectionComments|ResultsComments|BatchComments|EventCode|ProtocolCode|SampleAgency|GroupSamples|CollectionMethodName|Latitude|Longitude|CollectionDeviceDescription|CalibrationDate|PositionWaterColumn|PrepPreservationName|PrepPreservationDate|DigestExtractMethod|DigestExtractDate|AnalysisDate|DilutionFactor|ExpectedValue|LabAgency|SubmittingAgency|SubmissionCode|OccupationMethod|StartingBank|DistanceFromBank|UnitDistanceFromBank|StreamWidth|UnitStreamWidth|StationWaterDepth|UnitStationWaterDepth|HydroMod|HydroModLoc|LocationDetailWQComments|ChannelWidth|UpstreamLength|DownStreamLength|TotalReach|LocationDetailBAComments|SampleID|DW_AnalyteName|DataQuality|DataQualityIndicator|Datum|DataQualityIndicatorType|DataQualityIndicatorCode\n"
targetFile.write(header)

# open data file and read through lines
with open(dataFile, "r") as f:
    f.seek(0,0)
    for i,line in enumerate(f):
        line = line.strip()
        newLine = line + "||" + "\n"
        splitLine = line.split("|")
        try:
            # get data quality indicator value
            # if the value exists, iterate through indicators and parse for codes
            DQValue = splitLine[-2]
            if not DQValue:
                # empty field
                targetFile.write(newLine)
            else: 
                for ind in indicators:
                    startPosition = DQValue.find(ind)
                    if startPosition == -1:  
                        # not found
                        continue
                    else:
                        regex = ind + r'[: ]?([a-zA-Z0-9, /<>=]+)'
                        try:
                            # check if there is more than one code
                            # write new lines for each code
                            match = re.search(regex, DQValue).groups()
                            match = match[0]
                            if match.find(","):
                                matchCodes = match.split(",")
                            else: 
                                matchCodes = match
                            for code in matchCodes:
                                newLine = line + "|" + ind + "|" + code + "\n"
                                targetFile.write(newLine)
                        except:
                            # catch values that have indicator text (e.g. "Latitude:") but no codes
                            targetFile.write(newLine)
        except:
            # catch any lines that are missing the data quality indicator field
            targetFile.write(newLine)

targetFile.close()
print("Process complete!")