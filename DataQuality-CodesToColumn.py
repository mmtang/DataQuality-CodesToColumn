'''

California State Water Resources Control Board (SWRCB)
Office of Information Management and Analysis (OIMA) 

Michelle Tang (michelle.tang@waterboards.ca.gov)
https://github.com/mmtang

'''

import re

# change file if using a different dataset
dataFile = 'WaterChemistryData.csv'
targetName = 'new-file.csv'
targetFile = open(targetName, 'w')

print('Writing: ' + targetName)
print('Please wait...')

# write new header 
header = 'Program|ParentProject|Project|StationName|StationCode|SampleDate|CollectionTime|LocationCode|CollectionDepth|UnitCollectionDepth|SampleTypeCode|CollectionReplicate|ResultsReplicate|LabBatch|LabSampleID|MatrixName|MethodName|Analyte|Unit|Result|Observation|MDL|RL|ResultQualCode|QACode|BatchVerification|ComplianceCode|SampleComments|CollectionComments|ResultsComments|BatchComments|EventCode|ProtocolCode|SampleAgency|GroupSamples|CollectionMethodName|Latitude|Longitude|CollectionDeviceDescription|CalibrationDate|PositionWaterColumn|PrepPreservationName|PrepPreservationDate|DigestExtractMethod|DigestExtractDate|AnalysisDate|DilutionFactor|ExpectedValue|LabAgency|SubmittingAgency|SubmissionCode|OccupationMethod|StartingBank|DistanceFromBank|UnitDistanceFromBank|StreamWidth|UnitStreamWidth|StationWaterDepth|UnitStationWaterDepth|HydroMod|HydroModLoc|LocationDetailWQComments|ChannelWidth|UpstreamLength|DownStreamLength|TotalReach|LocationDetailBAComments|SampleID|DW_AnalyteName|DataQuality|DataQualityIndicator|Datum|DataQualityIndicatorType|DataQualityIndicatorCode\n'
targetFile.write(header)

count = 0

# open data file and read through lines
with open(dataFile, 'r') as imported:
    imported.seek(0,0)
    # skip header
    for _ in range(1):
        next(imported)
    for line in imported:
        line = line.strip()
        newLine = line + '||' + '\n'
        splitLine = line.split('|')
        DQValue = splitLine[-2]
        if not DQValue:
            # empty field
            targetFile.write(newLine)
            count += 1
        else: 
            indicators = DQValue.split(';')
            for ind in indicators:
                try:
                    # extract indicator type and codes
                    regexType = r'([a-zA-Z]+)[: ]?'
                    matchType = re.search(regexType, ind).groups()
                    matchType = matchType[0]
                    regexCode = matchType + r'[: ]?([a-zA-Z0-9, /<>=]+)'
                    matchCode = re.search(regexCode, ind).groups()
                    matchCode = matchCode[0]
                    codes = matchCode.split(',')
                    # write a new line for each code
                    for i in codes:
                        newLine = line + '|' + matchType + '|' + i + '\n'
                        targetFile.write(newLine)
                        count += 1
                except AttributeError:
                    # catch values that are missing codes
                    # 'Latitude:' is the main culprit here
                    # is 'Latitude' a data indicator type? need to check decision tree
                    targetFile.write(newLine)
                    count += 1

targetFile.close()
print('Finished writing %d records.' % (count)) 