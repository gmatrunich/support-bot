
import os
import json
import requests
import dialogflow_v2 as dialogflow
import logging
from dotenv import load_dotenv


load_dotenv()
DF_PROJECT_ID = os.environ['DF_PROJECT_ID']
LANGUAGE_CODE = 'ru'
JSON_FILE = "questions.json"


logger = logging.getLogger('telegram_logger')


def read_the_json_file(json_file):
    with open(json_file, "r", encoding="utf-8") as file:
        themes = json.load(file)
    return themes


def read_theme_info(theme):
    display_name = theme[0]
    training_phrases_parts = theme[1]['questions']
    message_texts = theme[1]['answer']
    return display_name, training_phrases_parts, message_texts


def create_intent(project_id, display_name, training_phrases_parts,
                  message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    response = intents_client.create_intent(
        parent, intent, language_code=LANGUAGE_CODE
        )

    print('Intent created: {}'.format(response))

    client = dialogflow.AgentsClient()
    parent = client.project_path(project_id)
    response = client.train_agent(parent)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger('Teach Logger')

    themes = read_the_json_file(JSON_FILE)
    for theme in themes.items():
        display_name, training_phrases_parts, message_texts = read_theme_info(
            theme
            )
        try:
            create_intent(
                DF_PROJECT_ID,
                display_name,
                training_phrases_parts,
                message_texts
                )
        except requests.exceptions.HTTPError as err:
            logger.warning(f'Something has gone wrong!\n{err}')
