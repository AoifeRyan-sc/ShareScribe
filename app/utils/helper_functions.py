# import datetime
import io
import base64
import openai
import pandas as pd
from dash import html, dash_table
import os
# from dotenv import load_dotenv
# load_dotenv()

def check_file(contents, filename):
    _, content_string = contents.split(',')
    file_extension = filename.split('.')[-1].lower()
    print("checking size")
    decoded = base64.b64decode(content_string)

    max_size = 25 * 1024 * 1024 # limit set by openai until I implement chunking 

    file_size = len(decoded)
    if file_size > max_size:
        return f'Error: {filename} exceeds the maximum file size of 25 MB.'
    elif file_extension not in ['wav', 'mp3', 'm4a']: # permitted file types
        return f'Error: Invalid file type. Please upload a .wav, .mp3, or .m4a file.'
    
    return decoded

def parse_contents(action, contents, response_format):
    _, content_string = contents.split(',')
    print("parse_content running")
    decoded = base64.b64decode(content_string)
    file_like = io.BytesIO(decoded)
    file_like.name = 'audio.m4a'

    api_key = os.getenv("OPENAI_API_KEY")
    # api_key = os.environ.get("OPENAI_API_KEY")
    
    client = openai.OpenAI(api_key = api_key)

    # if response_format in ("text"):
    #     api_output = getattr(client.audio, action).create(
    #     model="whisper-1", 
    #     file=file_like,
    #     response_format = "verbose_json",
    #     timestamp_granularities = "segment"
    #     )
    #     return api_output

    api_output = getattr(client.audio, action).create(
        model="whisper-1", 
        file=file_like,
        # response_format = response_format
        response_format = "srt"
    )

    return api_output

