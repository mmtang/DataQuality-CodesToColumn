This script reformats file outputs from [CEDEN_to_DataCaGov](https://github.com/CAWaterBoardDataCenter/CEDEN_to_DataCAGov). It parses concatenated codes in the 'DataQualityIndicator' field and rewrites them as separate records. The ouput file includes two new fields: 

(1) 'DataQualityIndicatorType'  = the code category (BatchVerification, Datum, QACode, ResultQualCode)<br />
(2) 'DataQualityIndicatorCode'  = the actual code (e.g. NR, VBY, VLC)

Requirements: Python 3.X
