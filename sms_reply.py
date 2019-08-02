from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio import twiml
from twilio.rest import Client

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    # Your Account SID from twilio.com/console
    account_sid = "<Twilio account_sid>"
    # Your Auth Token from twilio.com/console
    auth_token  = "Twilio authorization token"

    client = Client(account_sid, auth_token)


    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    # Checks to make sure message is from work.
    work_check = body[0:30]
    shift_type = body[37]
    shift_date = body[31:36]
    
    if work_check == 'Imminent Staffing Shift Offer:':
        if shift_type == 'N':
            if shift_date != 'Aug02' and shift_date != 'Aug04' and shift_date != 'Aug07':               
                index = body.rindex('Y')
                code = body[index:index+8]
                resp.message(code)
    if work_check == 'You have been awarded a shift.':
        message = client.messages.create(to="+1780<PERSONALNUMBER>",from_="+1587<TWILIONUMBER",body=body)
        print(message.sid)

    
    return str(resp)



if __name__ == "__main__":
    app.run(debug=True)


