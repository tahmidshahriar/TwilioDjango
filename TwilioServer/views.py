from django.shortcuts import render
import twilio.twiml
from django.views.decorators.csrf import csrf_exempt
import re
# Create your views here.


from penn.registrar import Registrar
from twilio.rest import TwilioRestClient
import requests

from django.http import HttpResponse

@csrf_exempt
def index(request):
    resp = twilio.twiml.Response()
    try:
        tempStr = request.POST["Body"]
        if (len(tempStr.split()) == 2):
            resp.message(text(tempStr.split()[0], tempStr.split()[1]))

        else:
            m = re.search("\d", tempStr)
            resp.message(text(tempStr[:m.start()], tempStr[m.start():]))

    except:
        resp.message("Hello")
        print "fail"

    return HttpResponse(resp)




def text(theName, theNumb):
    course = theName
    number = theNumb
    #phone = raw_input("Please enter phone number with country code.")
    courseForResponse = course.upper() + number

    #TWILIO ACCOUNT INFO GOES HERE
    account_sid = ""
    auth_token  = ""
    
    client = TwilioRestClient(account_sid, auth_token)

    #PENN INTOUCH REGISTRAR INFO GOES HERE, UPENN_##, AND PASSWORD (FOR REGISTRAR (r) AND THE RESPONSE'S AUTH)
    r = Registrar('', '')

    try:
        response = requests.get('https://esb.isc-seo.upenn.edu/8091/open_data/course_section_search?course_id=' + courseForResponse,
            auth = ("", ""))

    except:
        return "Course doesn't exist. Please retry with valid inputs (example: CIS 110)"

    notFail = True
    messageBody = ""

    try:
        firstSection = int((response.json()['result_data'][0])['section_number'])
    except:
        return "Course doesn't exist. Please retry with valid inputs (example: CIS 110)"

    messageBody = courseForResponse + " (" + (response.json()['result_data'][0])['course_title'] + ")"
    while (notFail):
        try:
            tempSec = str(firstSection)
            while (len(tempSec) < 3):
                tempSec = '0' + tempSec

            cis = r.section(course.lower(), number, tempSec)
            messageBody = messageBody + "\n" + "Section " + tempSec + " is " + cis['course_status_normalized']
            firstSection = firstSection + 1

        except:
            notFail = False

    return  messageBody

