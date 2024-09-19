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
    print("checking size")
    decoded = base64.b64decode(content_string)

    max_size = 25 * 1024 * 1024 # limit set by openai until I implement chunking 
    file_size = len(decoded)
    if file_size > max_size:
        return f'Error: {filename} exceeds the maximum file size of 25 MB.'
    
    return decoded

def parse_contents(action, contents, response_format):
    _, content_string = contents.split(',')
    print("parse_content running")
    decoded = base64.b64decode(content_string)

    file_like = io.BytesIO(decoded)
    file_like.name = 'audio.m4a'

    # api_key = os.getenv("OPENAI_API_KEY")
    api_key = os.environ.get("OPENAI_API_KEY")
    client = openai.OpenAI(api_key = api_key)

    # if response_format in ("xlsx", "json"):
    #     api_response_format = "verbose_json"
    #     kwargs = {"timestamp_granularities": ["segment"]}
        
    # else:
        # api_response_format = response_format
        # kwargs = {}

    # print(api_response_format)

    api_output = getattr(client.audio, action).create(
        model="whisper-1", 
        file=file_like,
        response_format = response_format
        # response_format= api_response_format,
        # **kwargs
    )

    # if response_format == "xlsx":
    #     results = []
    #     for i in range(len(api_output.segments)):
    #         df = pd.DataFrame({"start" : [api_output.segments[i]["start"]],
    #                         "text" : [api_output.segments[i]["text"]]})
    #         results.append(df)

    #     results = pd.concat(results)
    #     api_output = results
    #     print(type(results))

    return api_output

