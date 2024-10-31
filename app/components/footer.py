from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
from components import colour_mode_switch, colour_mode_callback

footer = html.Span([
     html.Hr(),
    dbc.Label("Live Performance Metrics", style = {"color": "white","font-weight":"light",'display' : 'flex','justifyContent': 'center'}),
    # html.Br(),
                dbc.Row(dbc.Col(html.Img(id = "footer-logo",
                                         src="./assets/SAMY_onwhite.png",
                                         style={
                                            'width': '100%',
                                            'height': '100%',
                                            'margin-top': '-20px'
                                            # 'margin': '10px'
                                        }),
                                width = {'size': 2}, align = "end"), justify = "end"),
])

def register_footer_callbacks(app):
    @app.callback(
        Output("footer-logo", "src"),
        Input("switch", "value")
    )
    def update_footer_logo(switch_value):
        if switch_value:
            return "./assets/SAMY_Logotipo-black.png"
        else:
            return   "./assets/SAMY_Logotipo-blanco.png"