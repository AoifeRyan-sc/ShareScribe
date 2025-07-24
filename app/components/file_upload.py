from dash import dcc, html
import dash_bootstrap_components as dbc


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
        # dbc.Button("Download Output", id = "download-button", color="secondary", className="mt-3", n_clicks = 0, style={'display': 'none'}),
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
            id = "output-type", value = "docx", inline = True,
            options = [
                {"label": "Document", "value": "docx"},
                {"label": "Subtitles", "value": "srt"}
        ]
        )
    ]),
    buttons_and_tooltip,
    dcc.Download(id="download-transcript")
])

error_message = html.Span([dbc.Row(dbc.Col(
    dcc.ConfirmDialog(
        id='error-message', message = [], displayed = False)
    ))])
