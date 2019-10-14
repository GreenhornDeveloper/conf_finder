from textblob import TextBlob

conversation_context = {
    'conference_info': {
        'parameters': ['event_locale', 'visitor_status'],
        'response_data': {
            'event_locale': {
                'raleigh': [
                    'You should look at the conference website <a href=https://www.raleighconvention.com/ target="blank"> Raleigh Convention Center</a>'
                ]
            },
        },
        'questions': {
            'event_locale': 'What conference location do you want to go to?',
            'visitor_status': 'Have you been here before?'
        }
    },
    'speaker_info': {
        'parameters': ['is_speaker_known', 'is_reviewing_speakers'],
        'questions': {
            'is_speaker_known': 'Do you know any of the speakers at the event?',
            'is_reviewing_speakers': 'Would you like find a speaker by name? If yes, type the speaker name:'
        }
    }
}


# Response Functions
def generate_response(query, intent, chat_session):
    query = query.lower()
    return collect_followup_data(query, intent, chat_session)


def collect_followup_data(query, intent, chat_session):
    # does a context exist?
    context_data = {}
    if 'context' in chat_session:
        # start follow up questions
        followup_param = chat_session['context_followup']
        chat_session['context_data'][followup_param] = query

        # see what questions were not asked
        context_data = chat_session['context_data']

    else:
        # start a context
        chat_session['context'] = intent
        chat_session['context_data'] = {}

    # ask follow-up questions
    for param in conversation_context[intent]['parameters']:
        if param not in context_data.keys():
            chat_session['context_followup'] = param
            return conversation_context[intent]['questions'][param], chat_session

    response = ''

    intent_map = {
        'conference_info': conference_response,
        'speaker_info': speaker_response
    }

    if intent in intent_map.keys():
        response = intent_map[intent](chat_session)

    chat_session = {}

    return response, chat_session


def conference_response(chat_session):

    intent = chat_session['context']
    context_data = chat_session['context_data']

    event_locale = context_data['event_locale']
    visitor_status = context_data['visitor_status']

    try:
        if visitor_status == 'no' or visitor_status == 'No':
            response = 'Im so glad you decided to visit {}! \n'.format(event_locale)
        else:
            response = 'Welcome back! I am sure you already know where to look, but if not, I will give you a hint.'
        for action in conversation_context[intent]['response_data']['event_locale'][event_locale]:
            response += ' {}\n'.format(action)

        return response
    except:
        return 'There was an error. Please contact the system administrator for further assistance.'


def speaker_response(chat_session):

    context_data = chat_session['context_data']

    is_speaker_known = context_data['is_speaker_known']
    is_reviewing_speakers = context_data['is_reviewing_speakers']

    if is_speaker_known == 'no' or is_speaker_known == 'No':
        if is_reviewing_speakers == 'no' or is_reviewing_speakers == 'No':
            response = 'You should look at the speaker list website <a href=https://allthingsopen.org/speakers/ target="blank"> ATO Speakers</a>'
        else:
            response = 'You should for that person here: <a href=https://allthingsopen.org/speakers/{} target="blank"> {}</a>'.format(is_reviewing_speakers.replace(" ", "-"), is_reviewing_speakers)
    else:
        if is_reviewing_speakers == 'no' or is_reviewing_speakers == 'No':
            response = ''

    return response
