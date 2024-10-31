from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
from components import colour_mode_switch, colour_mode_callback

footer = html.Span([
     html.Hr(),
    # html.Br(),
                dbc.Row(dbc.Col(html.Img(id = "footer-logo",
                                         src="./assets/SAMY_onwhite.png",
                                         style={
                                            'width': '100%',
                                            'height': '100%',
                                            'margin-top': '10px'
                                            # 'margin': '10px'
                                        }),
                                width = {'size': 2}, align = "end"), justify = "end"),
])

# making this a function that can be called in app.py and access 
# "switch-id" value - not sure if this is best practice or what is?
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