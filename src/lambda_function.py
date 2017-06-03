"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import random


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text=None, should_end_session=False):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    card_title = "Welcome"
    speech_output = "Welcome to Guess the Number. " \
                    "Please guess a number between 1 and 100 to begin." \
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please guess a number between 1 and 100 to begin."
    return build_response(session_attributes={}, build_speechlet_response(
        card_title, speech_output, reprompt_text))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for playing. " \
                    "Remember to like, favorite, comment, and subscribe. " \
                    "Have a nice day!"
    return build_response(session_attributes={}, build_speechlet_response(
        card_title, speech_output, should_end_session=True))


def create_target_number_attributes():
    return {"targetNumber": random.randint(1,100)}


def start_game(intent, session):
    card_title = intent['name']
    speech_output = "Let's play! I'm thinking of a number between 1 and 100... "
    reprompt_text = "You can say, take a guess."
    session_attributes = create_target_number_attributes()
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text))


def make_guess(intent, session):
    card_title = intent['name']
    session_attributes = session['attributes']

    if session.get('attributes', {}) and "targetNumber" in session.get('attributes', {}):
        target_number = session['attributes']['targetNumber']
        speech_output = "The target number is {}.".format(target_number)
        reprompt_text = "Please take another guess."
    else:
        speech_output = "Oops, you haven't started a game! " \
                        "You can say, let's play."
        reprompt_text = "Please start a game."
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "StartGameIntent":
        return start_game(intent, session)
    elif intent_name == "MakeGuessIntent":
        return make_guess(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.8f6884d0-eea8-41ff-9b80-a9fe4377932c"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
