from dash import Dash, Input, Output, State, html, callback
import dash_bootstrap_components as dbc
from utils import parse_contents
from components import colour_mode_switch, title_and_tooltip, file_upload_widget, footer, error_message

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, '/assets/custom.css'])
server = app.server
# app = Dash(__name__, external_stylesheets=[d bc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container([
    dbc.Row(dbc.Col(colour_mode_switch, width = 2, align = "end"), justify = "start"),
    dbc.Row(
        dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        title_and_tooltip,
                        file_upload_widget
                    ]),
                    className="mt-5"
                    ), width={"size": 6, "offset": 0}), 
                className="justify-content-center align-items-center h-100"
                ),
                error_message,
                footer,
], style={"height": "80vh"})



if __name__ == '__main__':
   app.server.run(port=8000, host='127.0.0.1', debug = True)
