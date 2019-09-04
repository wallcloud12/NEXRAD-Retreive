#####################################################
#                 NEXRAD DOWNLOAD                   #
#                                                   #
#                Michael P. Vossen                  #
#           Last Updated: May 8th, 2019             #
#                   Version 0.2                     #
#                                                   #
#                  Description                      #
# Program to download archived NEXRAD file from     #
# NCEI.  Askes user for the site id, date, and save #
# location for the files.  The program will output  #
# the data files into the directory specifed.       #
#                                                   #
#####################################################


#import packages
import urllib.request as ur
import requests
import os

#Menu print outs
print("NCEI NEXRAD Archive Download")

site = input("Enter Radar ID: ")
month = input("Enter Month: ")
day = input("Enter Day: ")
year = input("Enter Full Year: ")

start_hour = input("Enter Hour to Start Data Retreival: ")

finish_hour = input("Enter Hour to End Data Retreival: ")

savelocation = input("Enter Directory Path to Savelocation: ")

'''
zeropadremove

description:
    removes the padded zero from the front of dates and times
    
input:
    time (string)
    
output:
    (int)
'''

def zeropadremove(time):
    if len(time) == 2:
        if time[0] == "0":
            return (eval(time[1]))
        else:
            return (eval(time))
    else:
        return(eval(time))

'''
zeropadremove

description:
    checks if there is a padded zero in a date or time.  If the time
    or date is less than 10 it will add a padded zero if one does not
    already exist
    
input:
    time (string)
    
output:
    (string)
'''

def checkzeropad(time):
    if len(time) == 1:
        return("0" + time)
    else:
        return(time)
        


#make sure the dates have the zero padding if they are less than 10
#WILL NOT WORK IF THERE IS NO ZERO INFRONT OF NUMBERS LESS THAN 10
month = checkzeropad(month)
day = checkzeropad(day)

#make sure site id is upper case
#website url requires it to be upper case
site = site.upper()

#remove zero pad from the times given and make them integers above so logic can done later
start_hour = zeropadremove(start_hour)
finish_hour = zeropadremove(finish_hour)

#if user does not specify the save location it saves in the working directory
if savelocation == "":
    savelocation = os.getcwd()

#make sure directory path ends in /
if savelocation[len(savelocation)-1] != "/":
    savelocation = savelocation + "/"

#create name for new directory to save data in
newdirectory = site + "_" + month + "-" + day + "-" + year + "/"
newdirectory = savelocation + newdirectory

#if this new directory does not exist it will create it
#it will use the existing directory if it exists
if os.path.exists(newdirectory) == False:
    os.mkdir(newdirectory, 0o772)

#have the newdirectory become the save location
savelocation = newdirectory 

#this is done just for user error
#the later logic will include the ending hour's data
if finish_hour == "24":
    finish_hour = "23"
   
#downloads the website data
coded_url =ur.urlopen("https://www.ncdc.noaa.gov/nexradinv/bdp-download.jsp?id=" + site + "&yyyy=" + year + "&mm="+ month + "&dd=" + day + "&product=AAL2")

#decodes the website data to a readable format
website = coded_url.read().decode().splitlines()

#initate the terminate varable for latter
terminate = False

print("Starting Download")

#loop to download data
#it is definatly complicated. So, I will try to document the best I can

#loop starts at line 187 because that is where the data starts
#it ends at the end of the website array but has the ability to stop earlier
for line in range(187, len(website)):
    #if terminate = False it will continue to run
    #if terminate = True it will go down to the else statement to where there is a break command to end the loop
    if terminate == False:
        #check to see if there is any data in that line
        if len(website[line]) > 0:
            #if the line starts with <a href= it means that it is a website address
            if website[line][1:9] == "<a href=":
                #if the line has a / at character 11 it is a tar file at the end of the list of data files and the loop will end
                if website[line][11] != "/":
                    #start looking for the end character " at character 11
                    end = 11
                    #run through each index of the line till it finds the end character "
                    #once " is found the index is saved and will be used to slice out the website from the line
                    while website[line][end-1:end] != "\"":
                        end += 1
                        #lets face it if it hits index 2000 there is nothing there and we probaly hit the end of the list
                        #So, it will break out of the loop and terminate the whole download loop
                        if end == 2000:
                            terminate = True
                            break
                
                    #if the loop did not terminate earlier it will continue on                
                    if terminate == False:
                        #slice out the website url by using the end index found before
                        url = website[line][10:end-1]
                        #the file name is at the end of the url.  This is needed for saving the file later
                        filename = (url[59:len(url)])
                        #we are tring to find the hour of the file to make sure it's durring the time the user wants
                        #we need to check for that extra zero that starts hours less than 10 then make it an integer for logic later
                        if url[72] == "0":
                            hour = eval(url[73])
                        else:
                            #this a special case for some older files where the progam will go into the tar files at the end
                            #these tar files at 72:74 contain the string L2.  If this happens the loop will break and the data
                            #download will end because we are now through all of the data
                            if (url[72:74] == "L2"):
                                terminate = True
                                break
                            else:
                                hour = eval(url[72:74])
                        #if statement to check and see if data falls into time range before it tries to download the file
                        if hour >= start_hour and hour <= finish_hour:
                            #if it is in the time range it will request the url from the internet
                            r = requests.get(url)
                            #we take the data we got from the url request and write it to data file that is named the name
                            #we sliced out before
                            with open(savelocation + filename , 'wb') as fs:
                                fs.write(r.content)
                                
                        #if we are past the finish hour break out of the loop
                        if hour > finish_hour:
                            break
                #break out of the loop if there was a / at character 11. (described in detail above)
                else:
                    break
    #break out loop if terminate = true                           
    else:
        break

#end of program print out
print("Finished")
print("Files Saved To: " + savelocation)
            
        
            