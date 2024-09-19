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
    # print("".join(["parse contents :", action]))
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

    api_output = getattr(client.audio, action).create(
        model="whisper-1", 
        file=file_like,
        response_format= response_format,
        # response_format="verbose_json", # might add option for this but creates problems with timestamps for translations
        # timestamp_granularities=["segment"]
    )
    
    # if I wanted to make a table ----
    # results = []
    # for i in range(len(api_output.segments)):
    #     print(i)
    #     df = pd.DataFrame({"start" : [api_output.segments[i]["start"]],
    #                     "text" : [api_output.segments[i]["text"]]})
    #     results.append(df)
    #     # for key, value in transcript.segments[i].items():
    # results = pd.concat(results)
    # results.head()

    return api_output
# html.Div([
        # html.H5(filename),
        # html.H6(datetime.datetime.fromtimestamp(date)),
        # html.H6(transcription.text),  # Display the transcription text
        # html.H6(transcription.segments[1]),  # Display the transcription text
     
        # dash_table.DataTable(
        # data=results.to_dict('records'),  # Convert DataFrame to list of dictionaries
        # columns=[{"name": i, "id": i} for i in results.columns],  # Create columns metadata
        # style_table={'overflowX': 'auto'},  # Optional styling
    # ),
    # ])
