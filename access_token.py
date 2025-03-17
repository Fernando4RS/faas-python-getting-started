import requests

##
#   This code is provided by Dexcom. This is the way my code is able to access the API
#   All documentation and information are found in Dexcom's API. 
##

def getAccessToken():
  url = "https://sandbox-api.dexcom.com/v2/oauth2/token"

  payload = {
    "grant_type": "authorization_code",
    "code": "b487d96aba8fcd42e082bd58a3404c66", #This is the only value that has to change.
    "redirect_uri": "http://localhost:8000",
    "client_id": "lHsq840OLdWbjx1VEOl0IhLUoLQ4H70k", 
    "client_secret": "ecgk4CqL0Q2wl6lk",
  }


  headers = {"Content-Type": "application/x-www-form-urlencoded"}

  response = requests.post(url, data=payload, headers=headers)

  data = response.json() #This is the pain thing that we care about. This json response gives us the access token used in request_egv
  return data["access_token"], data["refresh_token"]

