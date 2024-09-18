from dash import Dash, Input, Output, State, html, callback
import dash_bootstrap_components as dbc
from utils import parse_contents
from components import colour_mode_switch, title_and_tooltip, file_upload_widget, footer

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

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
                footer,
                dbc.Row(dbc.Col(html.Div(id='output-data-upload'))) # need to get this out of here
], style={"height": "80vh"})



if __name__ == '__main__':
    # app.run_server(debug=True)
   app.server.run(port=8000, host='127.0.0.1', debug = True)
# from dash import Dash, dcc, html

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = Dash(__name__, external_stylesheets=external_stylesheets)
# app.layout = html.Div([
#     dcc.Upload(html.Button('Upload File')),

#     html.Hr(),

#     dcc.Upload(html.A('Upload File')),

#     html.Hr(),

#     dcc.Upload([
#         'Drag and Drop or ',
#         html.A('Select a File')
#     ], style={
#         'width': '100%',
#         'height': '60px',
#         'lineHeight': '60px',
#         'borderWidth': '1px',
#         'borderStyle': 'dashed',
#         'borderRadius': '5px',
#         'textAlign': 'center'
#     })
# ])

# if __name__ == '__main__':
#     app.server.run(port=8000, host='127.0.0.1', debug = True)
