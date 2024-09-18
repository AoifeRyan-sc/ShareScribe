from dash import html
import dash_bootstrap_components as dbc

footer = html.Span([
     html.Hr(),
    dbc.Label("Live Performance Metrics", style = {"color": "white","font-weight":"light",'display' : 'flex','justifyContent': 'center'}),
    # html.Br(),
                dbc.Row(dbc.Col(html.Img(src="./assets/SHARE_onwhite.png",
                                         style={
                                            'width': '100%',
                                            'height': '100%',
                                            # 'margin': '10px'
                                        }),
                                width = {'size': 2}, align = "end"), justify = "end"),
])