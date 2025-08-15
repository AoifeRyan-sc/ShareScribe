from dash import dcc, html
import dash_bootstrap_components as dbc
from utils import language_codes, info_popover, language_selection_dropdown


title_and_tooltip = html.Span([
    dbc.Row([
    dbc.Col([
        html.H2("SAMY Audio Transcriber", id="page-title", className="text-center mb-4 d-inline-block", style={"white-space": "nowrap"}),
        info_popover(text_id = "title-tooltip-hover", icon_id= "title-tooltip", popover_text= "Currently only accepting .wav, .mp3, and .m4a files, contact the Data Science team to add to compatible formats. If you have a video file you would like to transcribe, you can export as `audio only` from QuickTime (and other apps)."),
    ], className="d-flex justify-content-center align-items-center", width={"size": 6, "offset": 3})
])
])

buttons_and_tooltip = html.Span([
    dbc.Row([
    dbc.Col([
        dbc.Button("Process Audio", id = "go-button", color="primary", className="mt-3", n_clicks = 0, style={"font-weight": "normal"}),
    ], className="d-flex justify-content-center align-items-center", 
    )
])
])

word_exclusions = html.Span([
    dbc.Label("Words in the audio file you do not want translated:", html_for="no-translate-title", className="mb-2 d-block"),
    dcc.Input(
    id = "no-translate-words",
    placeholder = "SAMY UK, McLaren, Diageo...",
    style = {'width': '100%'}
    )
],
id = "word-exclusions",
style={'display': 'none'}
)

language_translation_selection = html.Span([
    language_selection_dropdown(id = "translate-from-dropdown", label = "Translate from..."),
    language_selection_dropdown(id = "translate-to-dropdown", label = "Translate to...")
],
id = "select-translation-language",
style={'display': 'none'}
)

language_transcription_selection = html.Span([
    language_selection_dropdown(id = "transcribe-from-dropdown", label = "Audio language"),
],
id = "select-transcription-language",
style={'width': '100%', 'display': 'flex', 'fontSize': '16px', 'paddingTop': '10px', 'gap': '10px'}
)

file_upload_widget = html.Span([
    dcc.Upload(
        ['Drag-and-Drop or ', html.A('Select Files')],
        id = "upload-data",
        multiple = False
    ),
    dcc.Store(id = "stored-filename"),
    html.Div(id='spinner-fast-trigger', style={'display': 'none'}), # this is to make the file upload spinner appear immediately
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
    language_translation_selection,
    language_transcription_selection,
    word_exclusions,
    html.Div([
        html.Label("Select export format:", className = "mt-3"),
        dbc.RadioItems(
            id = "output-type", value = "docx", inline = True,
            options = [
                {"label": "Document (.docx)", "value": "docx"},
                {"label": "Subtitles (.srt)", "value": "srt"}
        ]
        )
    ]),
    buttons_and_tooltip,
    dcc.Download(id="download-transcript") # should probably move the location of this
])

error_message = html.Span([dbc.Row(dbc.Col(
    dcc.ConfirmDialog(
        id='error-message', message = [], displayed = False)
    ))])
