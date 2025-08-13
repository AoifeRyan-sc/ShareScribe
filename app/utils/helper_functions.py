# import datetime
import io
import base64
import openai
import pandas as pd
# from dash import html, dash_table
import os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re

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

def translate_transcription(parsed_file, language_to, language_from, words):

    transcribed_text = parsed_file

    pattern = r', ?'

    words_split = re.split(pattern, words)
    words_list = [no_translation] + words_split
    words_quote_list = [f"'{word}'" for word in words_list]
    ", ".join(words_quote_list)

    spanish_response_srt = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Below is an srt with {language_from} text. Translate it to an srt in {language_to}. Don't translate words that don't have a {language_to} translation, some examples are: {words_not_for_translation}. \n\n {transcription_srt}"
    )



def srt_to_docx(srt_string):

    doc = Document()

    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(11)

    entries = re.split(r'\n\n', srt_string.strip())

    for entry in entries:
        lines = entry.split('\n')
        # if len(lines) >= 3:  # Ensure we have at least timestamp and text?
        timestamp = lines[1]
        text = ' '.join(lines[2:])

        p = doc.add_paragraph()

        timestamp_run = p.add_run(timestamp + " ")
        timestamp_run.font.color.rgb = RGBColor(192, 192, 192)  # Light grey

        # wrapped_text = textwrap.wrap(text, width=60)  # Adjust width as needed
        p.add_run(lines[2])
    
    byte_stream = io.BytesIO()
    doc.save(byte_stream)
    byte_stream.seek(0)  

        # for line in wrapped_text[1:]:
            # p.add_run('\n' + ' ' * 8 + line)

        # p.paragraph_format.space_after = Pt(6)  # Space after paragraph

    return byte_stream
