from dash import dcc, html
import dash_bootstrap_components as dbc

output_card = html.Span([
    html.H2("Transcription Output"),
    # html.H5("50% width card", className="card-title"),
    html.P(
        id = "api_output_text",
        className="card-text",
        children = "this is a test",
        style={'whiteSpace': 'pre-wrap'}
    )
])

download_button_test = html.Span(
    dbc.Button(
        "Download Output",
        id="download-button-test",
        color="secondary", 
        className="mt-3", 
        n_clicks = 0, 
        style={
            "display": "none",
            "position": "absolute",
            "bottom": "230px",
            "right": "80px",
            "z-index": "10"
        }
    )
)
