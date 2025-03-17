from flask import Flask, render_template
import time
import json
import requests as requests
from turbo_flask import Turbo
from threading import Thread
##from waitress import serve

from request_egv import get_egv

## Initialize the Flask app. This is based on the basic examples of Flask API
app = Flask(__name__) 

## Initialize Turbo class for our Flask App. This will allow us to send updates in realt time.
turbo = Turbo(app)

## Initialize the main page. "/" is the URI we will be working on. So at the end this will show 
## in url: http://127.0.0.1:8000/
@app.route("/", methods=['GET'])
def index():
    ##render_templates, as the name implies, renderizes into the server a base template http found in the folder templates
    return render_template('base_templ.html', datapoints=datapoints, datatimes=datatimes)


## Similarly as above, this initializes the URI "/data" as of now, the microcontroller is pulling from here. the data is just an entire
## string where the data is shown
@app.route("/data", methods=['GET'])
def data():
    RefreshTokenInd = 0
    SavedRefreshToken = ""
    Header_AccessToken = ""
    datapoints, datatimes, dict_egv, csv_format, RefreshTokenInd, SavedRefreshToken, Header_AccessToken= get_egv(RefreshTokenInd, SavedRefreshToken, Header_AccessToken)  # Fetch the latest data

    return json.dumps(csv_format) ## dumps all the info found in dict_egv into http://127.0.0.1:8000/data

## This function is the main part of how the data is updated in real time:
def update_load():
    ## used as a with block, the app.app_context allows us to push a context and run a code outside of the app main code, 
    ## in other words, this allows us to  update the data datapoints, datatimes every X amount of time. In this demo, 10 secs
    RefreshTokenInd = 0
    SavedRefreshToken = ""
    Header_AccessToken = ""
    with app.app_context():
        while True: ## mantains an infinite loop, letting our code to run forever

            global datapoints, datatimes
            datapoints, datatimes, dict_egv, csv_format, RefreshTokenInd, SavedRefreshToken, Header_AccessToken= get_egv(RefreshTokenInd, SavedRefreshToken, Header_AccessToken)  # Fetch the latest data
            print("refresh token Counter: ", RefreshTokenInd)
            print(f"{datapoints[0]}, {datatimes[0]}\n\n") #This is just for debugging purposes
            ## 'turbo.push' allows us to push an update to our data. Since this is under the app_context, the data will update automatically
            ## without having to refresh or do anything to the code or webpage
            time.sleep(60) # Update every 10 seconds
            turbo.push(turbo.replace(render_template('data_points.html', datapoints = datapoints), 'datapoints'))
            turbo.push(turbo.replace(render_template('data_times.html', datatimes = datatimes), 'datatimes'))

if __name__ == "__main__":
    ## We create a thread that runs our function 'update_load' above. so we can dynamically change the data and run the Flask app at
    # the same time.
    Thread(target=update_load, daemon=True).start()
    app.run(debug=False, host='0.0.0.0', port=8000, threaded=True) #Runs the Flask App
    
