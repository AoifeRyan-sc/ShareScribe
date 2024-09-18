from dash import Input, Output, html, clientside_callback
import dash_bootstrap_components as dbc

colour_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch"),
        dbc.Switch(
            id="switch",
            value=True,
            className="d-inline-block ms-1",
            persistence=True
        ),
        dbc.Label(className="fa fa-sun", html_for="switch")
    ]
)

colour_mode_callback = clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute("data-bs-theme", switchOn ? "light" : "dark"); 
       return window.dash_clientside.no_update
    }
    """,
    Output("switch", "id"),
    Input("switch", "value"),
)