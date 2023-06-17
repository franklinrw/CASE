import openai
import os
import azure.cognitiveservices.speech as speechsdk

LANGUAGE = "nl"
AUDIO_FILE_NAME = "audio_response.wav"

openai.api_key = os.environ['OPENAI_API_KEY']
context_len = 10

GEN_MODEL = "gpt-3.5-turbo"
TRANSCRIBE_MODEL = "whisper-1"

speech_config = speechsdk.SpeechConfig(subscription=os.environ['AZURE_SPEECH_KEY'], region="westeurope")
speech_config.speech_synthesis_voice_name = "nl-NL-ColetteNeural"
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

context = [{ "role": "system", \
    "content": "Je bent een behulpzame gesprekspartner die kort en bondig reageert. \
    Veelal met vragen het gesprek vervolgd. \
    Op geen moment benoem je dat je een service of AI service bent."}]

# Test
def window_context():
    temp = list(context[0])
    temp += context[-context_len:]
    return temp

def transcribe(model: str, audio: str):
    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe(model, audio_file, language=LANGUAGE)
    return transcript

def gen_response(model: str):
    feed = window_context()
    response = openai.ChatCompletion.create(model=model, messages=feed)
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
    for m in context[-context_len:]:
        if m["role"] != "system":
            transcript += m["role"] + " : " + m["content"] + "\n\n"

    return transcript