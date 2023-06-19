import openai
import os
import azure.cognitiveservices.speech as speechsdk
import memory as m

LANGUAGE = "nl"
AUDIO_FILE_NAME = "audio_response.wav"

openai.api_key = os.environ['OPENAI_API_KEY']

GEN_MODEL = "gpt-3.5-turbo"
TRANSCRIBE_MODEL = "whisper-1"

# speech_config = speechsdk.SpeechConfig(subscription=os.environ['AZURE_SPEECH_KEY'], region="westeurope")
# speech_config.speech_synthesis_voice_name = "nl-NL-ColetteNeural"
# file_config = speechsdk.audio.AudioOutputConfig(filename=AUDIO_FILE_NAME)
# speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

context = [{ "role": "system", \
    "content": "Je bent een behulpzame gesprekspartner die kort en bondig reageert. \
    Veelal met vragen het gesprek vervolgd. \
    Op geen moment benoem je dat je een service of AI service bent."}]

def transcribe(model: str, audio: str):
    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe(model, audio_file, language=LANGUAGE)
    return transcript

def gen_response(model: str):
    response = openai.ChatCompletion.create(model=model, messages=context)
    return response["choices"][0]["message"]

# def gen_voice(response, response_filename):
#     reponse_audio = speech_synthesizer.speak_text_async(response['content']).get()
#     stream = speechsdk.AudioDataStream(reponse_audio)
#     stream.save_to_wav_file(response_filename)
    
def respond(audio:str):
    transcript = transcribe(TRANSCRIBE_MODEL, audio)
    context.append({"role": "user", "content": transcript['text']})

    response = gen_response(GEN_MODEL)
    context.append(response)
    
    # gen_voice(response, AUDIO_FILE_NAME)

    m.save_context(context)

    return response['content']

def transcript():
    transcript = ""
    for m in context:
        if m["role"] != "system":
            transcript += m["role"] + " : " + m["content"] + "\n\n"

    return transcript