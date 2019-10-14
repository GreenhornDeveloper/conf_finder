from flask import Flask, session, render_template
from flask import request
from flask_cors import CORS
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier, DecisionTreeClassifier
import uuid
import chatbotUtils as chatbot

app = Flask(__name__)
CORS(app, resources={
    r"/*": {"origins": ["http://localhost:5000", "http://0.0.0.0:5000"]}})

train = [
    ("Are there any conferences in town?", 'conference_info'),
    ("What time are the local conferences?", 'conference_info'),
    ("Where do I go for conference or event info?", 'conference_info'),
    ("How do I know when events occur at the conference center?", 'conference_info'),
    ("Are there any conferences at the convention center today?", 'conference_info'),
    ("If someone wants to know about local events, what do they do?", 'conference_info'),
    ("Where do I find out information regarding events at the convention center?", 'conference_info'),
    ("Who are the speakers at the conference?", 'speaker_info'),
    ("Who is speaking at All Things Open?", 'speaker_info'),
    ("What person is giving a session at the conference?", 'speaker_info'),
    ("What are the names of the speakers at the conference?", 'speaker_info'),
    ("Which speaker is giving a talk at all things open?", "speaker_info"),
    ("Are there going to be speakers at the all things open conference?", "speaker_info")
]

cl_nb = NaiveBayesClassifier(train)


@app.route("/")
def main():
    return render_template('index.html', id_data=uuid.uuid4())


chat_session = {}


def context_builder(question_data, id_data):
    user_intent = cl_nb.classify(question_data)

    if id_data in chat_session.keys():
        user_intent = chat_session[id_data]['context']
    else:

        chat_session[id_data] = {}

    response, new_chat_session = chatbot.generate_response(question_data, user_intent, chat_session[id_data])

    if len(new_chat_session) == 0:
        del chat_session[id_data]
        response += '!OVER!'
    else:
        for key, value in new_chat_session.items():
            chat_session[id_data][key] = value
    return response


@app.route("/api/askChatbot", methods=["POST"])
def talk_to_chatbot():
    user_response = request.json
    question_data = user_response.get("user_response", "notFound")
    id_data = user_response.get("user_identifier", "notFound")
    return context_builder(question_data, id_data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT", 5000))
