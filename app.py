#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# = = = = = = = #
#NOTE: the below code makes the whole webhook crash...can't understand why -_- #

import gspread
#from oauth2client.service_account import ServiceAccountCredentials

#gspread credentials

#json_key = 'gspread-test.json'
#scope = ['https://spreadsheets.google.com/feeds']

#credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

#gc = gspread.authorize(credentials)

#spr = gc.open_by_key("1_afG4TmSYG6v1hJxcIWc5hyXMMZbFxXzL9-0856DXmU")

#wks = spr.worksheet("Sheet1")

# = = = = = = = #

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "start.date":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    country = parameters.get("Offices-Locations")
    month = parameters.get("Startdates-months")

    dates = {"France":'July 3rd', "UK":'July 3rd or 31st'}

    speech = "The possible start-date(-s) for " + country + " in " + month + " are " + str(dates[country])

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-startdates"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
