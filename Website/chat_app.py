import dash
from dash import Dash, Input, Output, State
from dash import html

import dash_bootstrap_components as dbc

from chat_app_util import split_text

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        html.H1("ComradeChat", style={"text-align": "center"}),
        html.Div(
            [
                html.Div(
                    [
                        html.Br(),
                        html.Div(
                            id="conversation",
                            style={
                                "max-height": "500px",
                                "overflow-x": "hidden",
                                "overflow-y": "scroll",
                                "display": "flex",
                                "flex-direction": "column-reverse",
                            },
                        ),
                        html.Br(),
                        html.Table(
                            [
                                html.Tr(
                                    [
                                        # user text input
                                        html.Td(
                                            [
                                                dbc.Input(
                                                    id="msg_input",
                                                    placeholder="Type Here . . .",
                                                    type="text",
                                                    style={"width": "80%"},
                                                )
                                            ],
                                            style={"width": "100%", "valign": "middle"},
                                        ),
                                        # send user text
                                        html.Td(
                                            [
                                                dbc.Button(
                                                    "Send",
                                                    id="send_button",
                                                    type="submit",
                                                    #style={"width": "100%"},
                                                )
                                            ],
                                            style={"width": "100%", "valign": "middle"},
                                        ),
                                    ]
                                )
                            ]
                        ),
                    ],
                    style={"margin": "0 auto"},
                )
            ],
            id="screen",
            style={"width": "800px", "height": "500px", "margin": "0 auto"},
        ),
    ]
)


# callback for when user sends a message
@app.callback(
    [
        Output("conversation", "children"),
        Output("msg_input", "value"),
    ],
    [
        Input("send_button", "n_clicks"),
        State("conversation", "children"),
        State("msg_input", "value"),
    ],
    prevent_initial_call=True,
)
def process_message(n_clicks, history, text):
    # Put the text processing/response stuff here?

    # temporary place holder response
    temp_response = {
        "description": "Here is a place holder for a basic description of what has been found based off the return, do something or whatever!",
        "title": "Here is the title of the link provided",
        "dataset_url": "https://www.google.ca/",
    }

    response_text = split_text(temp_response["description"])
    user_text = split_text(text)

    user_msg = [
        html.P(user, style={"text-align": "right", "margin": "1px"})
        for user in user_text
    ]
    response_msg = [
        html.P(html.I(res), style={"text-align": "left", "margin": "1px"})
        for res in response_text
    ]

    response_url = ""
    if "title" in temp_response and "dataset_url" in temp_response:
        response_url = [
            html.P(
                html.A(temp_response["title"], href=temp_response["dataset_url"]),
                style={"text-align": "left", "margin": "1px"},
            )
        ]

    if history:
        # order reversed so new lines always appear at the bottom in combiantion with CSS
        return (
            response_url
            + response_msg
            + ["ComradeChat Bot:"]
            + user_msg
            + [html.Hr(style={"width": "100%"})]
            + history,
            "",
        )
    return response_url + response_msg + ["ComradeChat Bot:"] + user_msg, ""


# run Dash app
if __name__ == "__main__":
    app.run_server()
