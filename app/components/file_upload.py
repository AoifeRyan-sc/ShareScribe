from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
from utils import parse_contents, check_file
from dash.exceptions import PreventUpdate

title_and_tooltip = html.Span([
    dbc.Row([
    dbc.Col([
        html.H2("Share Audio Transcriber", id="page-title", className="text-center mb-4 d-inline-block", style={"white-space": "nowrap"}),
        dbc.Label(className="fa fa-circle-info ms-2 d-inline-block", id="title-tooltip", html_for="page-title", style={"position": "relative", "top": "-1mm", 'color': '#7800c6'}),
        dbc.Tooltip(
            "Currently only accepting m4a files (can export videos as 'audio only'), contact Data Science team to add compatible formats",
            id="tooltip",
            is_open=False,
            target="title-tooltip",
            placement="right"
        )
    ], className="d-flex justify-content-center align-items-center", width={"size": 6, "offset": 3})
])
])

file_upload_widget = html.Span([
    dcc.Upload(
        ['Drag and Drop or ', html.A('Select Files')],
        id = "upload-data",
        multiple = False, accept = '.m4a', max_size = 25 * 1024 * 1024 # in bytes
    ),
    dbc.Spinner(html.Div(id = "loading-output")),
    html.Div(id = "upload-status"),
    dbc.Spinner(dcc.Download(id="download-transcript"), 
                spinner_style= {'border-color': '#bb7fe2', 'border-right-color': 'transparent'}),
    dbc.Progress(value=0, style={"margin-top": "20px", "margin-bottom": "20px", "height": "20px"}),
    dbc.RadioItems(
        id = "action-input", value="transcriptions", inline = True, className = "2mt-3",
        options = [
            {"label": "Transcription", "value": "transcriptions"},
            {"label": "Translation", "value": "translations"}
        ]
    ),
    html.Div([
        html.Label("Select export format:", className = "mt-3"),
        dbc.RadioItems(
            id = "output-type", value = "srt", inline = True,
            options = [
                {"label": "srt", "value": "srt"},
                {"label": "doc", "value": "text"},
                {"label": "json", "value": "json"} # what other formats are available?
            # {"label": "xlsx", "value": "xlsx"} # do I want this?
        ]
        )
    ]),
    dbc.Button("Process Video", id = "go-button", color="primary", className="mt-3", n_clicks = 0),
    # dbc.Spinner(html.Div(id = "process-file-spinner", color = "primary")),
    # dbc.Button("Download Transcript", id = "download-button", color="secondary", className="mt-3", n_clicks = 0),
])

error_message = html.Span([dbc.Row(dbc.Col(
    dcc.ConfirmDialog(
        id='error-message', message = [], displayed = False)
    ))])

@callback(
        Output('error-message', 'displayed'),
        Output('error-message', 'message'),
        Output("download-transcript", "data"),
        Output("go-button", "n_clicks"),
        Input('go-button', 'n_clicks'),
        State('action-input', 'value'),
        State('output-type', 'value'),
        State('upload-data', 'contents'),
        State('upload-data', 'filename'),
        prevent_initial_call=True
        )
def update_output(n_clicks, action, response_format, content, name):

    if content is not None and n_clicks > 0:
        print("content not none")
        check_output = check_file(content, name)

        if type(check_output) == str:
            return True, check_output, None, 0
        
        children = [
            parse_contents(action, content, response_format)
        ]
        return False, None, dict(content=children, filename="".join({"transcript.", response_format})), 0

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
    
    return None, f"Uploaded file: {filename}"

# @callback(Output('confirm-danger', 'displayed'),
#           Input('dropdown-danger', 'value'))
# def display_confirm(value):
#     if value == 'Danger!!':
#         return True
#     return False
