from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
from utils import parse_contents, check_file, srt_to_docx
from dash.exceptions import PreventUpdate

title_and_tooltip = html.Span([
    dbc.Row([
    dbc.Col([
        html.H2("SHARE Audio Transcriber", id="page-title", className="text-center mb-4 d-inline-block", style={"white-space": "nowrap"}),
        dbc.Label(className="fa fa-circle-info ms-2 d-inline-block", id="title-tooltip", html_for="page-title", style={"position": "relative", "top": "-1mm", 'color': '#7800c6'}),
        dbc.Tooltip(
            "Currently only accepting .wav, .mp4, and .m4a files, contact the Data Science team to add to compatible formats. If you have a video file you would like to transcribe, you can export as `audio only` from QuickTime (and other apps).",
            id="title-tooltip-hover",
            is_open=False,
            target="title-tooltip",
            placement="right"
        )
    ], className="d-flex justify-content-center align-items-center", width={"size": 6, "offset": 3})
])
])

buttons_and_tooltip = html.Span([
    dbc.Row([
    dbc.Col([
        dbc.Button("Process Video", id = "go-button", color="primary", className="mt-3", n_clicks = 0),
        dbc.Button("Download Transcript", id = "download-button", color="secondary", className="mt-3", n_clicks = 0),
        dbc.Label(className="fa fa-circle-info ms-2 d-inline-block", id="download-tooltip", html_for="page-title", style={"position": "relative", "top": "3mm", 'color': '#ffb600'}),
        dbc.Tooltip(
            "If you want to save to a custom filepath, you will have to enable this in your browser download settings.",
            id="download-tooltip-hover",
            is_open=False,
            target="download-tooltip",
            placement="right"
        )
    ], className="d-flex justify-content-center align-items-center", 
    # width={"size": 6, "offset": 3}
    )
])
])

file_upload_widget = html.Span([
    dcc.Upload(
        ['Drag and Drop or ', html.A('Select Files')],
        id = "upload-data",
        multiple = False
    ),
    dbc.Spinner(html.Div(id = "loading-output")),
    html.Div(id = "upload-status", style={"margin-top": "20px", "margin-bottom": "20px", "height": "20px"}),
    dbc.Spinner(dcc.Store("processed_file"), spinner_style= {'border-color': '#bb7fe2', 'border-right-color': 'transparent'}),
    dbc.Progress(value=0, style={"margin-top": "20px", "margin-bottom": "20px", "height": "20px"}),
    dbc.RadioItems(
        id = "action-input", value="transcriptions", inline = True, className = "2mt-3",
        options = [
            {"label": "Transcribe", "value": "transcriptions"},
            {"label": "Transcribe & Translate", "value": "translations"}
        ]
    ),
    html.Div([
        html.Label("Select export format:", className = "mt-3"),
        dbc.RadioItems(
            id = "output-type", value = "srt", inline = True,
            options = [
                {"label": "Subtitles", "value": "srt"},
                {"label": "Document", "value": "docx"}
        ]
        )
    ]),
    buttons_and_tooltip,
    dcc.Download(id="download-transcript"),
     dbc.Modal(
        [
            dbc.ModalHeader("Processing Complete"),
            dbc.ModalBody(html.Div(id = "modal_message")),
        ],
        size="xl",
        id="processing-complete-modal",
        is_open=False,
    ),
])

error_message = html.Span([dbc.Row(dbc.Col(
    dcc.ConfirmDialog(
        id='error-message', message = [], displayed = False)
    ))])



@callback(
        Output('error-message', 'displayed'),
        Output('error-message', 'message'),
        Output('upload-data', 'contents'),
        Output('upload-data', 'filename'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        prevent_initial_call=True
        )
def file_check_callback(content, name):
    
    if content is not None:
        print("file check callback")
        check_output = check_file(content, name)

        if type(check_output) == str:
            return True, check_output, None, None

    return False, None, content, name

@callback(
        Output("processed_file", "children"),
        Output("go-button", "n_clicks"),
        Output('processing-complete-modal', 'is_open'),
        Output('modal_message', 'children'),
        Input('go-button', 'n_clicks'),
        State('action-input', 'value'),
        State('output-type', 'value'),
        State('upload-data', 'contents'),
        prevent_initial_call=True
        )
def update_output(n_clicks, action, response_format, content):
    print("update output function working")

    if content is not None and n_clicks > 0:
        print("update output function processing")
        
        processed_file =  parse_contents(action, content, response_format)

        return processed_file, 0, True, processed_file
    return None, 0, False, None

@callback(
    Output("loading-output", "children"),
    Output("upload-status", "children"),
    Input("upload-data", "contents"),
    Input("processed_file", "children"),
    State("upload-data", "filename"),    
    prevent_initial_call=True
)
def show_upload_progress(contents, file_state, filename):

    if file_state is not None:
        return None, f"Processed file: {filename}, press Download button to save"
    elif contents is None:
        raise PreventUpdate
    
    return None, f"Uploaded file: {filename}"

@callback(
    Output("download-transcript", "data"),
    Input("download-button", "n_clicks"),
    State('output-type', 'value'),
    State("processed_file", "children"),
    State("upload-data", "filename"),    
)
def download_file(n_clicks, response_format, processed_data, filename):
    
    if n_clicks > 0:
        # if response_format == "text":
        #     response_format = "doc"
        download_title = "".join([filename, response_format])
        print(download_title)

        if response_format == "docx":
            byte_stream = srt_to_docx(processed_data)
            
            return dcc.send_bytes(
                byte_stream.getvalue(),
                download_title
            )
        
        return dict(content=processed_data, filename=download_title)


