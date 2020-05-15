import translator
import json
import os


def lambda_handler(event, context):

    print(event)
    
    s3_key = event['key']
    source_language_code = event['source_language_code']
    request_id = event['request_id']

    print(s3_key)

    #Transcribe:
    #bucketName = os.environ['BucketName']
    bucketName = 'voice-translator-translatorbucket-kvuovdlq7o4a'
    job_uri = 's3://' + bucketName + '/' + s3_key
    job_name = request_id
    
    print(job_uri)
    print(job_name)
    transcript = translator.transcribe(job_name, job_uri, source_language_code)

    if transcript == "" :
        raise Exception('Transcript is empty')

    source_language_code = 'zh'
    #Result:
    codes = {
        'EnglishUS': {
            'translate_code': 'en',
            'polly_code': 'en-US',
        },
        'French': {
            'translate_code': 'fr',
            'polly_code': 'fr-FR',
        },
        'Japanese' : {
            'translate_code': 'ja',
            'polly_code': 'ja-JP',
        },
        'Korean' : {
            'translate_code': 'ko',
            'polly_code': 'ko-KR'
        }
    }

    for language in codes:
        
        #Translate:
        print(language)
        codes[language]['translate_text'] = translator.translate(
            transcript, 
            source_language_code, 
            codes[language]['translate_code'])

        print(codes[language]['translate_text'])

        #Polly:
        codes[language]['polly_url'] = translator.polly(
            codes[language]['translate_text'],
            codes[language]['polly_code'],
            request_id)
        
        print(codes[language]['polly_url'])

    codes['transcript'] = transcript

    return codes
