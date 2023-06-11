import openai
import os
import azure.cognitiveservices.speech as speechsdk

LANGUAGE = "nl"
AUDIO_FILE_NAME = "audio_response.wav"

openai.api_key = os.environ['OPENAI_API_KEY']

GEN_MODEL = "gpt-3.5-turbo"
TRANSCRIBE_MODEL = "whisper-1"

speech_config = speechsdk.SpeechConfig(subscription=os.environ['AZURE_SPEECH_KEY'], region="westeurope")
speech_config.speech_synthesis_voice_name = "nl-NL-ColetteNeural"
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

context = [{ "role": "system", \
"content": "Je bent een Nederlandse Tutor die gebruikers bijstaat om de Nederlandse taal te leren en te oefenen. \
        Dit zal je doen doormiddel van dialogen en gesprekken die geleidelijk in complexiteit stijgt. \
        Zorg voor een mix van open en gesloten vragen om de gebruiker uit te dagen en te betrekken. \
        Corrigeer fouten in het Nederlands van de gebruiker op een bemoedigende manier om het leren te bevorderen. \
        Focus op het creëren van een natuurlijke en menselijke interactie."}]

def transcribe(model: str, audio: str):
    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe(model, audio_file, language=LANGUAGE)
    return transcript

def gen_response(model: str):
    response = openai.ChatCompletion.create(model=model, messages=context)
    return response["choices"][0]["message"]

def gen_voice(response, response_filename):
    reponse_audio = speech_synthesizer.speak_text_async(response['content']).get()
    stream = speechsdk.AudioDataStream(reponse_audio)
    stream.save_to_wav_file(response_filename)
    
def respond(audio:str):
    transcript = transcribe(TRANSCRIBE_MODEL, audio)
    context.append({"role": "user", "content": transcript['text']})

    response = gen_response(GEN_MODEL)
    context.append(response)
    
    gen_voice(response, AUDIO_FILE_NAME)

    return AUDIO_FILE_NAME

def transcript():
    transcript = ""
    for m in context:
        if m["role"] != "system":
            transcript += m["role"] + " : " + m["content"] + "\n\n"

    return transcript