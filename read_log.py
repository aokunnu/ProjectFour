FILE_NAME = './local_copy.log'

import re
from datetime import datetime, timedelta, date
import calendar
from collections import Counter

#Create the counters
last = 0
total = 0
all_requests = 0
mondays = 0
tuesdays = 0
wednesdays = 0 
thursdays = 0 
fridays = 0
saturdays = 0
sundays = 0
mon_number = 0
tue_number = 0
wed_number = 0
thu_number = 0
fri_number = 0
sat_number = 0
sun_number = 0
error_4xx =  0
error_3xx = 0

seperate_files = {}
dates = {}

#Regex used to split up the lines for each log file
regex = re.compile(r".*\[([^:]*):(.*) \-[0-9]{4}\] \"([A-Z]+) (.+?) (HTTP.*\"|\") ([2-5]0[0-9]) .*")
for line in open(FILE_NAME):
    repl = line.replace("[", "#", 10).replace(":", "#", 10).replace("/", "#", 10)
    year = repl.split('#')
    total += 1
    if len(year)>=3:
        if year[3] == str(1995):
             last += 1
#This will split the regex into the necessary elements 
elements = regex.split(line)

#Checks to see if the regex worked and bypasses error
if len(elements) < 3:

#Creates the days of the week, adds to the counters, and counts the number of requests per day
    date = datetime.strptime(elements[1], "%d/%b/%Y")
    weekday = date.isoweekday()
    if weekday == 1:
        mondays += 1
    if weekday == 2:
        tuesdays += 1
    if weekday == 3:
        wednesdays += 1
    if weekday == 4:
        thursdays += 1
    if weekday == 5:
        fridays += 1
    if weekday == 6:
        saturdays += 1
    if weekday == 7:
        sundays += 1
    
#Calculates error code percentages 
error_code = elements[6]
all_requests += 1
if int(error_code) >= 400 and int(error_code) <= 499:
    error_4xx += 1
if int(error_code) >= 300 and int(error_code) <= 399:
    error_3xx += 1
#Coverts error code totals
error_4xx = (error_4xx/all_requests)*100
error_3xx = (error_3xx/all_requests)*100

#Creates a dictionary to track how many times a file is requested
filename = elements[4]
if filename in seperate_files:
    seperate_files[filename] += 1
else:
    seperate_files[filename] = 1

#Creates a dictionary to track how many times each day of the week happens 
days = elements[1]
if days in dates:
    dates[days] += 1
else:
    dates[days] = 1

#Takes the keys from the date dictionary and makes them date objects 
dates_list = list(dates.keys())
for i in dates_list:
    date_object = datetime.strptime(i, "%d/%b/%Y")
    day_of_week = date_object.isoweekday()
    #This will increase the counters for the days of the week
    if day_of_week == 1:
        mon_number += 1
    if day_of_week == 2:
        tue_number += 1
    if day_of_week == 3:
        wed_number += 1
    if day_of_week == 4:
        thu_number += 1
    if day_of_week == 5:
        fri_number += 1
    if day_of_week == 6:
        sat_number += 1
    if day_of_week == 7:
        sun_number += 1

print("The total number of requests made on Mondays:", mondays)
print("The total amount of requests made on Tuesdays:", tuesdays)
print("The total amount of requests made on Wednesdays:", wednesdays)
print("The total amount of requests made on Thursdays:", thursdays)
print("The total amount of requests made on Fridays:", fridays)
print("The total amount of requests made on Saturdays:", saturdays)
print("The total amount of requests made on Sundays:", sundays)
print("")
print("There were ", last, "total requests made in the last year.")
print("There were ", total, "total requests made in the time period represented by the log.")
print("")
print("The percentage of redirected requests was:", error_3xx,)
print("The percentage of unsuccessful requests per week:", error_4xx)
print("")
print("The most requested file was:", sorted(seperate_files, key = seperate_files.get, reverse = True)[:1])
print("The least requested file was:", sorted(seperate_files, key = seperate_files.get, reverse = False)[:1])
