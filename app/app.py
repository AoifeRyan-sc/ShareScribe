from dash import Dash, Input, Output, State, html, callback
import dash_bootstrap_components as dbc
from utils import parse_contents
# from components import colour_mode_switch, title_and_tooltip, file_upload_widget, footer, error_message, register_footer_callbacks, register_all_callbacks, output_card, download_button
import components as cp

external_stylesheets = [
   dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME
]


app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = dbc.Container([
    dbc.Row(dbc.Col(cp.colour_mode_switch, width = 2, align = "end"), justify = "start"),
    dbc.Row(
    [
        dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    cp.title_and_tooltip,
                    cp.file_upload_widget
                ]
            ),
            id = "upload-card",
            className = "mt-5",
            # style = {"height": "400px"}
        ),
        width={"size": 6, "offset": 0}
        ),
        dbc.Col(
            [
                dbc.Card(
                    [
                        dbc.CardBody(
                        cp.output_card
                        ),
                        cp.download_button
                    ],
                    id = "display-card",
                    className = "mt-5",
                    style={'height': '400px', "overflowY": "scroll"}
                ),
            ],
            style = {"display": None, 'position': 'relative'},
            id = "display-col",
        )
    ],
    className="justify-content-center align-items-center h-100",
    ),
        cp.file_error_message,
        cp.language_error_message,
        cp.footer,
    ], style={"height": "80vh"})

cp.register_all_callbacks(app)
cp.register_footer_callbacks(app)

if __name__ == '__main__':
   app.server.run(port=8000, host='127.0.0.1', debug = True)


