from dash import Dash, Input, Output, State
from dash import html

import dash_bootstrap_components as dbc

from api.api import API
from chat_app_util import split_text, format_responses

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

api = API("resources/datasets.json")

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
                                                    placeholder="Type Here...",
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
                                                    style={"width": "100%"},
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
    response_final = format_responses(api.generate_response(text, maximum_num_responses=4))

    user_text = split_text(text)
    user_msg = [
        html.P(user, style={'text-align': 'right',
                            "border-radius": "15px",
                            "background-color": "rgb(52, 58, 64)",
                            "color": "white",
                            "padding": "10px",
                            "margin-left": "auto"}
        ) 
        for user in user_text
    ]

    response_final.reverse()
    response_final = [html.P(response_final, style={'text-align': 'left',
                            "border-radius": "15px",
                            "background-color": "rgb(232, 232, 232)",
                            "color": "#212529",
                            "padding": "10px",
                            "margin-right": "auto"})]

    if history:
        # order reversed so new lines always appear at the bottom in combiantion with CSS
        return (
            response_final
            + ["ComradeChat Bot:"]
            + user_msg +
            [html.Hr(style={'width': '100%'})] +
            history,
            ''
        )
    return response_final + ["ComradeChat Bot:"] + user_msg, ''

# run Dash app
if __name__ == "__main__":
    app.run_server()
