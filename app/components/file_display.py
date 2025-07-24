from dash import dcc, html
import dash_bootstrap_components as dbc

output_card = html.Span([
    html.H2("Transcription Output"),
    html.Div(
        html.P(
            id = "api_output_text",
            className="card-text",
            children = "this is a test",
            style={
                'height': '280px',
                'overflow-y': 'auto',
                'padding-right': '50px'  # Space for button
            }
        ),
            style={'whiteSpace': 'pre-wrap'}
        )
    # )
])

download_button = html.Span(
    dbc.Button(
        "Download Output",
        id="download-button",
        color="secondary", 
        n_clicks = 0, 
        style={
                'position': 'absolute',
                'bottom': '10px',
                'right': '10px',
                'z-index': '1000'
            }
    )
)
