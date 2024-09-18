from dash import Dash, dcc, html, Input, Output, State, callback, dash_table, clientside_callback
import dash_bootstrap_components as dbc
import base64
import datetime
import io
import openai
import pandas as pd
from dash.exceptions import PreventUpdate
import os
from dotenv import load_dotenv
load_dotenv()


# import dash
# from dash import html, dcc, Input, Output, clientside_callback
# import dash_bootstrap_components as dbc

# Initialize the app with Bootstrap theme and Font Awesome icons
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
color_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch"),
        dbc.Switch(
            id="switch",
            value=True,
            className="d-inline-block ms-1",
            persistence=True
        ),
        dbc.Label(className="fa fa-sun", html_for="switch")
    ]
)

app.layout = dbc.Container([
    dbc.Row(dbc.Col(color_mode_switch, width = 2, align = "end"), justify = "start"),
    dbc.Row(
        dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dbc.Row([dbc.Col(html.H2("Share Audio Transcriber", id = "page-title", className="text-center mb-4"),className="d-flex justify-content-center"),
                                dbc.Col([dbc.Label(className="fa fa-circle-info", id = "title-tooltip", html_for="page-title"),
                                        dbc.Tooltip("Currently only accepting m4a files (can export videos as 'audio only'), contact Data Science team to add compatible formats",
                                            id="tooltip",
                                            is_open=False,
                                            target="title-tooltip",
                                            placement = "right"
                                            )], className="d-flex justify-content-center", width={"size": 6, "offset": 3}
                                        )
                                ]),
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or ', html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                # 'margin': '10px'
                            },
                            multiple = False,
                            accept='.m4a' # let's extend this list
                        ),
                        dbc.Spinner(html.Div(id="loading-output")),
                        html.Div(id="upload-status"),
                        dbc.Progress(value=0, style={"margin-top": "30px", "height": "7px"}),
                        dbc.RadioItems(
                           id = "action-input",
                            options=[
                                {"label": "Transcription", "value": "transcriptions"},
                                {"label": "Translation", "value": "translations"}
                            ],
                            value="transcription",
                            inline=True,
                            className="mt-3"
                        ),
                        html.Div([
                            html.Label("Select export format:", className="mt-3"),
                            dbc.RadioItems(
                                options=[
                                    {"label": "JSON", "value": "json"},
                                    {"label": "SRT", "value": "srt"},
                                    {"label": "TSV", "value": "tsv"},
                                    {"label": "TXT", "value": "txt"},
                                    {"label": "VTT", "value": "vtt"},
                                    {"label": "DOCX", "value": "docx"}
                                ],
                                value="json",
                                inline=True
                            )
                        ]),
                        dbc.Button("Process Video", color="primary", className="mt-3"),
                        dbc.Button("Download Transcript", color="secondary", className="mt-3")
                    ]),
                    className="mt-5"
                    ), width={"size": 6, "offset": 0}), 
                # justify="center"
                className="justify-content-center align-items-center h-100"
                ),
                dbc.Row(dbc.Col(html.Img(src="assets/SHARE_onwhite.png",
                                         style={
                                            'width': '100%',
                                            'height': '100%',
                                            # 'margin': '10px'
                                        }),
                                width = {'size': 2}, align = "end"), justify = "end"),
                dbc.Row(dbc.Col(html.Div(id='output-data-upload')))
], style={"height": "80vh"})

clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute("data-bs-theme", switchOn ? "light" : "dark"); 
       return window.dash_clientside.no_update
    }
    """,
    Output("switch", "id"),
    Input("switch", "value"),
)


def parse_contents(action, contents, filename, date):
    content_type, content_string = contents.split(',')
    print("".join(["parse contents :", action]))

    # Decode base64 string to binary
    decoded = base64.b64decode(content_string)

    # Initialize OpenAI API key (no need to create a client object)
    api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI(api_key = api_key)

    # Use io.BytesIO to create a file-like object from the decoded binary
    # file_like = io.StringIO(decoded.decode("utf-8"))
    file_like = io.BytesIO(decoded)
    file_like.name = 'audio.m4a'

    api_output = getattr(client.audio, action).create(
        model="whisper-1", 
        file=file_like,
        response_format="srt",
        # response_format="verbose_json", # might add option for this but creates problems with timestamps for translations
        # timestamp_granularities=["segment"]
    )
    
    results = []
    for i in range(len(api_output.segments)):
        print(i)
        df = pd.DataFrame({"start" : [api_output.segments[i]["start"]],
                        "text" : [api_output.segments[i]["text"]]})
        results.append(df)
        # for key, value in transcript.segments[i].items():
    results = pd.concat(results)
    results.head()

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        # html.H6(transcription.text),  # Display the transcription text
        # html.H6(transcription.segments[1]),  # Display the transcription text
     
        dash_table.DataTable(
        data=results.to_dict('records'),  # Convert DataFrame to list of dictionaries
        columns=[{"name": i, "id": i} for i in results.columns],  # Create columns metadata
        style_table={'overflowX': 'auto'},  # Optional styling
    ),

        html.Hr(),  # horizontal line

        # Display a snippet of the raw content for debugging
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@callback(
        Output('output-data-upload', 'children'),
        #   Input('action-input', 'value'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        State('upload-data', 'last_modified')
        )
def update_output(list_of_contents, list_of_names, list_of_dates):
    # print("".join(["list of contents: ", list_of_contents]))
    print("werking")
    if list_of_contents is not None:
        # print(action)
        action = "translations"
        children = [
            parse_contents(action, list_of_contents, list_of_names, list_of_dates)
            # parse_contents(action, c, n, d) 
            # for c, n, d in
            # zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children

@callback(
    Output("loading-output", "children"),
    Output("upload-status", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=True
)
def show_upload_progress(contents, filename):
    if contents is None:
        raise PreventUpdate
    print("working with an o")
    
    return None, f"Uploaded file: {filename}"

if __name__ == '__main__':
    # app.run_server(debug=True)
   app.server.run(port=8000, host='127.0.0.1', debug = True)
