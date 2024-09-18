from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
from utils import parse_contents
from dash.exceptions import PreventUpdate

title_and_tooltip = html.Span([
    dbc.Row([
        dbc.Col(
            html.H2(
                "Share Audio Transcriber", id = "page-title", className="text-center mb-4"
            ),
            className="d-flex justify-content-center"
        ),
        dbc.Col([
            dbc.Label(className="fa fa-circle-info", id = "title-tooltip", html_for="page-title"),
            dbc.Tooltip("Currently only accepting m4a files (can export videos as 'audio only'), contact Data Science team to add compatible formats",
                        id="tooltip",
                        is_open=False,
                        target="title-tooltip",
                        placement = "right")
        ], className="d-flex justify-content-center", width={"size": 6, "offset": 3})
    ])
])

file_upload_widget = html.Span([
    dcc.Upload(
        ['Drag and Drop or ', html.A('Select Files')],
        id = "upload-data",
        multiple = False, accept = '.m4a', max_size = 25e6
    ),
    dbc.Spinner(html.Div(id = "loading-output")),
    html.Div(id = "upload-status"),
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
                {"label": "SRT", "value": "srt"},
                {"label": "DOC", "value": "doc"}
            # {"label": "xlsx", "value": "xlsx"} # do I want this?
        ]
        )
    ]),
    dbc.Button("Process Video", id = "go-button", color="primary", className="mt-3", n_clicks = 0),
    dbc.Button("Download Transcript", color="secondary", className="mt-3", n_clicks = 0)
])


@callback(
        Output('output-data-upload', 'children'),
        #   Input('action-input', 'value'),
        Input('go-button', 'n_clicks'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        State('upload-data', 'last_modified')
        )
def update_output(n_clicks, content, name, date):
    if content is not None and n_clicks > 0:
        action = "transcriptions"
        children = [
            parse_contents(action, content, name, date)
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
    
    return None, f"Uploaded file: {filename}"