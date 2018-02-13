#https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
 
 
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name(sys.argv[1], scope)
client = gspread.authorize(creds)
 
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open(sys.argv[2]).sheet1
 
# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)
