import requests

##
#   This code is provided by Dexcom. This is the way my code is able to access the API
#   All documentation and information are found in Dexcom's API. 
##

def Refresh_Token(RefreshToken):
  
  url = "https://sandbox-api.dexcom.com/v2/oauth2/token"

  payload = {
    "grant_type": "refresh_token",
    "refresh_token": RefreshToken, #This is the only value that has to change.
    "client_id": "lHsq840OLdWbjx1VEOl0IhLUoLQ4H70k", 
    "client_secret": "ecgk4CqL0Q2wl6lk",
  }


  headers = {"Content-Type": "application/x-www-form-urlencoded"}

  response = requests.post(url, data=payload, headers=headers)

  data = response.json() #This is the pain thing that we care about. This json response gives us the access token used in request_egv
  return data["access_token"], data["refresh_token"]

