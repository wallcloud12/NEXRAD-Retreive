# NEXRAD-Retreive
## Description
A program that retrieves archived NEXRAD data from NCEI’s AWS bucket.  Currently the program is only able to download one day of data at a time. (00 UTC - 00 UTC)

## Instructions
1. Run code with a python interpreter
2. Enter the radar site ID (e.g. KMPX)
3. Enter the month number for the desired date
4. Enter the day for the desired date
5. Enter the year for the desired date. (yyyy)
6. Enter the hour in UTC on the date specified you would like to start the download
7. Enter the hour in UTC on the date specified you would like to end the download
8. Enter the directory path to where the data should save. (Defaults to current working directory)
