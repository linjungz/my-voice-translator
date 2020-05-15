import boto3
import time
import urllib
import json
import logging

bucket_name = 'voice-translator-translatorbucket-kvuovdlq7o4a'


def transcribe(job_name, job_uri, language_code):
    mytranscribe = boto3.client('transcribe')
    mytranscribe.start_transcription_job(TranscriptionJobName=job_name, Media={'MediaFileUri': job_uri}, MediaFormat='wav', LanguageCode=language_code)

    while True:
        status = mytranscribe.get_transcription_job(TranscriptionJobName=job_name)
        #print(status)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Transcribe job not yet ready")
        time.sleep(10)

    print(status)

    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        response = urllib.request.urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
        data = json.loads(response.read())
        text = data['results']['transcripts'][0]['transcript']
        print('Transcript: ' + text)
        return text
    
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED':
        raise Exception('Transcription Job Failed')

def translate(text, source_language_code, target_language_code):
    mytranslate = boto3.client('translate')

    response = mytranslate.translate_text(
    Text=text,
    SourceLanguageCode= source_language_code,
    TargetLanguageCode= target_language_code)
    print('Response: ', response)

    return response['TranslatedText']

def polly(text, language_code, request_id):
    mypolly = boto3.client('polly')
    mys3 = boto3.client('s3')

    polly_codes = {
        'en-US': {
            'VoiceId' : 'Joanna',
            'Engine' : 'neural'
        },
        'fr-FR': {
            'VoiceId' : 'Celine',
            'Engine' : 'standard'
        },
        'ja-JP': {
            'VoiceId' : 'Mizuki',
            'Engine' : 'standard'
        },
        'ko-KR': {
            'VoiceId' : 'Seoyeon',
            'Engine' : 'standard'
        }
    }

    response = mypolly.synthesize_speech(
        VoiceId = polly_codes[language_code]['VoiceId'],
        Engine = polly_codes[language_code]['Engine'],
        OutputFormat = "mp3",
        Text = text)

    print(response)

    file = open('/tmp/speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()

    key = 'output/' + request_id + '-' + language_code + '.mp3'

    mys3.upload_file('/tmp/speech.mp3', bucket_name, key)
    presigned_url = mys3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket' : bucket_name,
            'Key' : key
        })
    
    return presigned_url