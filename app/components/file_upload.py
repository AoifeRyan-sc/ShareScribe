from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
from utils import parse_contents, check_file, srt_to_docx
from dash.exceptions import PreventUpdate

title_and_tooltip = html.Span([
    dbc.Row([
    dbc.Col([
        html.H2("SAMY Audio Transcriber", id="page-title", className="text-center mb-4 d-inline-block", style={"white-space": "nowrap"}),
        dbc.Label(className="fa fa-circle-info ms-2 d-inline-block", id="title-tooltip", html_for="page-title", style={"position": "relative", "top": "-1mm", 'color': '#1C7E75'}),
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
        dbc.Button("Process Audio", id = "go-button", color="primary", className="mt-3", n_clicks = 0, style={"font-weight": "normal"}),
        dbc.Button("Download Output", id = "download-button", color="secondary", className="mt-3", n_clicks = 0, style={'display': 'none'}),
    ], className="d-flex justify-content-center align-items-center", 
    # width={"size": 6, "offset": 3}
    )
])
])

file_upload_widget = html.Span([
    dcc.Upload(
        ['Drag-and-Drop or ', html.A('Select Files')],
        id = "upload-data",
        multiple = False
    ),
    dcc.Store(id = "stored-filename"),
    dbc.Spinner(html.Div(id = "loading-output")),
    html.Div(id = "upload-status", style={"margin-top": "20px", "margin-bottom": "20px", "height": "20px"}),
    dbc.Spinner(dcc.Store("processed_file"), spinner_style= {'border-color': '#1C7E75', 'border-right-color': 'transparent'}),
    dbc.Progress(value=0, style={"margin-top": "20px", "margin-bottom": "20px", "height": "10px"}),
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
                {"label": "Document", "value": "doc"},
                {"label": "Subtitles", "value": "srt"}
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
        Input('go-button', 'n_clicks'),
        State('upload-data', 'filename'),
        prevent_initial_call=True
        )
def file_check_callback(content, nclicks, name):
    print("nclicks: ", nclicks)

    if content is None and nclicks > 0:
        print("checking file upload")
        return True, f'No file uploaded', None, None
 
    if content is not None:
        print("file check callback")
        check_output = check_file(content, name)

        if type(check_output) == str:
            return True, check_output, None, None

    return False, None, content, name

@callback(
        Output("processed_file", "data"),
        # Output("go-button", "n_clicks"),
        Output('processing-complete-modal', 'is_open'),
        Output('modal_message', 'children'),
        Input('go-button', 'n_clicks'),
        State('action-input', 'value'),
        State('output-type', 'value'),
        State('upload-data', 'contents'),
        prevent_initial_call=True
        )
def update_output(n_clicks, action, response_format, content):

    if content is not None and n_clicks > 0:
        print("update output function processing")
        
        processed_file =  parse_contents(action, content, response_format)

        # return processed_file, 0, True, processed_file #, False, None
        return processed_file, True, processed_file #, False, None
    # return None, 0, False, None#, False, None
    return None, False, None#, False, None

# @callback(
#         Output("processed_file", "data"),
#         Input("upload-data", "filename"),
#         State("stored-filename", "children"),
#         # State("processed_file", "data"),
#         prevent_initial_call=True
# )
# def update_file_state(current_filename, previous_filename):

#     if (current_filename != previous_filename) & (previous_filename is not None):
#         print("happening")
#         update_file_state = None
#         print(update_file_state)
#         return update_file_state
#         # return file_state

#     # return None
    
#     # else:
#     #     return None


@callback(
    Output("loading-output", "children"),
    Output("upload-status", "children"),
    Output("stored-filename", "data"),
    # Output("stored-filename", "data"),
    Input("upload-data", "contents"),
    Input("processed_file", "data"),
    State("upload-data", "filename"),
    State("stored-filename", "data"),    
    prevent_initial_call=True
)
def show_upload_progress(contents, file_state, filename, stored_name):
    print(stored_name)
    print(filename)

    if (filename != stored_name) & (stored_name is None):
        print("setting")
        print(stored_name)
        stored_name = filename
        print(stored_name)

    if (filename != stored_name) & (stored_name is not None):
        stored_name = filename
        print("resetting")
        file_state = None

    if file_state is not None:
        return None, f"Processed file: {filename}, press Download button to save", stored_name
    
    elif contents is None:
        raise PreventUpdate
    
    return None, f"Uploaded file: {filename}", stored_name

@callback(
    Output("download-transcript", "data"),
    Input("download-button", "n_clicks"),
    State('output-type', 'value'),
    State("processed_file", "data"),
    State("upload-data", "filename"),    
)
def download_file(n_clicks, response_format, processed_data, filename):
    
    if n_clicks > 0:
        file_name = filename.split('.')[0].lower()
        download_title = "".join([file_name,".", response_format])
        print(download_title)

        if response_format == "docx":
            byte_stream = srt_to_docx(processed_data)
            
            return dcc.send_bytes(
                byte_stream.getvalue(),
                download_title
            )
        
        return dict(content=processed_data, filename=download_title)


@callback(
    Output('download-button', 'style'),
    Input('processed_file', 'data'),
)
def show_download_button(processed_file):
    if processed_file is not None:
        return {'display': 'inline-block'}  # Make button visible
    return {'display': 'none'} 


# @callback(
#     Output('download-button', 'children'),
#     Output('current-filename', 'children'),
#     Input('upload-data', 'contents'),
#     Input('upload-data', 'filename'),
#     Input('processed_file', 'children'),
#     State('current-filename', 'data'),
#     prevent_initial_call=True
# )
# def download_button_visibility(contents, new_filename, processed_file, stored_filename):

#      if processed_file is not None:
#         return {'display': 'inline-block'}  # Make button visible
#     return {'display': 'none'} 


#     if contents is None:
#         return {'display': 'none'}, None
    
#     if new_filename != stored_filename: # If filename changed, hide button
#         return {'display': 'none'}, new_filename
    
#     # Otherwise, keep button visible
#     return {'display': 'none'}, new_filename
