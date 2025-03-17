import requests
from datetime import datetime, timedelta, timezone
import numpy as np
from access_token import getAccessToken
from refreshtoken import Refresh_Token


##Here we access the main thing we need from Dexcome, which are the Estimated Glucove Values, or EGVs. 
url = "https://sandbox-api.dexcom.com/v3/users/self/egvs"

## In the header, we put the authorization token we got from "access_token.py". This token grants us access to the Dexcom Sancbox for 2 hours.
## This can be extended by using the 'refresh_token'. 
##
## Note: 'refresh_token' is yet to be implemented in this code


###########################    get_egv()     #################################
# get_egv(): Given the access token and url locally defined above, get_egv() will return:
# egv:              All EGV values ranging from start_date to end_date
# datetime_egv:     Date and hour when the EGV was read. 
# dict_egv:         Dictionary that relates a date and an egv one to one
def get_egv(RefreshTokenTimer, SavedRefreshToken, savedAccessToken):
  ## function allows proxy server to read the time of this computer as of right now, interpret it in UTC since the DSE only accepts UTC
  ##
  ## Since at a minimum we need 288 datapoints, the start date is set 26 hours prior to the host computer clock, and the end date is set
  ## 1 hour in the future. This gurantees the latest data from DSE.
  now = datetime.now(timezone.utc)
  ## start_date: The start time of get_egv dataset. As of now, I have it a little over a day in the past as a buffer to ensure that
  ##             all data from a day ago is gathered.
  ## end_date: The end time of  get_egv dataset. As of now, my code looks into 1 hour into the future. This data has not been
  ##           produced by the emulator yet. However, serves as a buffer to when the data is updated in the emulator 
  ##
  ## Finally strftime allows us to format the start and end date based on how DSE API requires for us to succesfully gather the data€‹‹

# This snipet of code was added 02/24/2025, it automizes the process of getting the access token!
  start_date = (now + timedelta(hours=-27)).strftime("%Y-%m-%dT%H:%M:%S") 
  end_date = (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")

  ## The following if/else statements deal with the entire logic of creating and accessing either the access token or use the refresh token provided!
  ## Note, even though there are some handlelers, This code most likely don't have all handles required to detect a problem and bugs might appear on the long run
  ## This code was only tested in intervals of 5 mins to verify that the access token and the refresh token were set up correctly and run smoothly
  ## More testing must be done where the code is let to run for prolonged periods of time.
  # 
  ## IMPORTANT: ONLY CHANGE THE ELIF STATEMENT     IN LINE 51     TO CHANGE THE TIME OF WHEN TO USE THE REFRESH TOKEN AGIAN.
  #  

  if(RefreshTokenTimer == 0):
    print("Starting App, Access Token has been obtained!")
    AccessToken, RefreshToken = getAccessToken()
    Header_AccessToken = "Bearer " + AccessToken  
  elif(RefreshTokenTimer >= 100):
    if(SavedRefreshToken == ""):
      print("Something went wrong and saved RefreshToken was not saved")
      return False, False, False, False, False, False
    else:
      print("Time To reset AccessToken!")
      AccessToken, RefreshToken=Refresh_Token(SavedRefreshToken)
      Header_AccessToken = "Bearer " + AccessToken
      RefreshTokenTimer = 1
  else:
    RefreshToken = SavedRefreshToken
    Header_AccessToken = savedAccessToken
     

  headers = {"Authorization": Header_AccessToken}
## the query to request data from Dexcom services. provided by Dexcom's API
  query = {
    "startDate": start_date,
    "endDate": end_date
  }

  ##response is the confirmation that the data from the 'start_date' to the 'end_date' was requested and provided
  response = requests.get(url, headers=headers, params=query) 
  data = response.json() ## saves the data in a local variable
  n_datapoints = 20 ## we gather 288 points. Every egv is registered every 5 mins. Therefore (24*60)/5 
  egv = [0]*n_datapoints 
  datetime_egv = [0]*n_datapoints
  csv_format = [0]*n_datapoints*2
  ## now, since data not only contains the egv and datetime when that egv was gathered, we run a for loop to gather the latest
  ## 288 egvs and datetimes in the data gathered. 

  if "fault" in data:
    print("Something went wrong. . .")
    print("Error: ", data["fault"])
    return 0, 0, 0, 0, RefreshTokenTimer + 1, RefreshToken, Header_AccessToken
  
  else:
    for i in range(n_datapoints):
      egv[i] = data["records"][n_datapoints-i]["value"]
      input_datetime = data["records"][n_datapoints-i]["displayTime"]

      pst_to_cst = datetime.fromisoformat(input_datetime)
      adjusted_dt = pst_to_cst + timedelta(hours=3) ## 
      output_datetime = adjusted_dt.strftime("%m/%d/%Y_%H:%M:%S") ##Sets the date time in the desired format
      datetime_egv[i] = output_datetime

      datetime_egv_csv = adjusted_dt.strftime("%Y%m%d%H%M%S")

      csv_format[i+i] = data["records"][n_datapoints - i]["value"]
      csv_format[i+i-1] = int(datetime_egv_csv)

    dict_egv = dict(zip(datetime_egv, egv)) 
    return egv, datetime_egv, dict_egv, csv_format, RefreshTokenTimer + 1, RefreshToken, Header_AccessToken
  

#datapoints, datatimes, dict_egv, csv_format, RefreshTokenInd, SavedRefreshToken = get_egv(0, "")

#print(csv_format, RefreshTokenInd, SavedRefreshToken)

#datapoints, datatimes, dict_egv, csv_format, RefreshTokenInd, SavedRefreshToken = get_egv(200, SavedRefreshToken)

#print(csv_format, RefreshTokenInd, SavedRefreshToken)