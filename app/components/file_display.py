from dash import dcc, html
import dash_bootstrap_components as dbc

# going to sunset this display option
output_popup = html.Span([ 
    dbc.Modal(
        [
            dbc.ModalHeader("Processing Complete"),
            dbc.ModalBody(html.Div(id = "modal_message")),
        ],
        size="xl",
        id="processing-complete-modal",
        is_open=False,
    )
])

output_card_init = html.Span([
    # dbc.Card(
    #         dbc.CardBody(
    #             [
                    html.H5("50% width card", className="card-title"),
                    html.P(
                        [
                            "This card uses the ",
                            html.Code("w-50"),
                            " class to set the width to 50%",
                        ],
                        className="card-text",
                    ),
        #         ]
        #     ),
        #     className="w-50",
        # )
])

output_card = html.Span([
    html.H2("Transcription Output"),
    # html.H5("50% width card", className="card-title"),
    html.P(
        id = "modal_message_test",
        className="card-text",
        children = "this is a test"
    )
])