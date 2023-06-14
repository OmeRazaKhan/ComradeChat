import dash
from dash import Dash, Input, Output, State
from dash import html

from chat_app_util import split_text, format_responses
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

temp_res = [
    {
        "ranking": 1,
        "dataset_id": 31,
        "dataset_url": "https://open.canada.ca/data/en/dataset/3ac0d080-6149-499a-8b06-7ce5f00ec56c",
        "dataset_description": "The description of the most relevant dataset to the user's query",
        "message": "A message outputted by the backend describing any information to the user if needed",
        "resources": [
            {
                "title": "Resource 1 title",
                "download_url": "https://open.canada.ca/data/dataset/id_31_dataset_1.csv",
                "data_format": "csv",
                "languages": ["en", "fr"],
            },
            {
                "title": "Resource 2 title",
                "download_url": "https://open.canada.ca/data/dataset/id_31_dataset_2.json",
                "data_format": "json",
                "languages": ["en"],
            },
        ],
    },
    {
        "ranking": 2,
        "dataset_id": 7,
        "dataset_url": "https://open.canada.ca/data/en/dataset/e33bcd95-d0e5-4ade-9f5c-78f0a5a4d7a0",
        "dataset_description": "The description of the most relevant dataset to the user's query",
        "message": "A message outputted by the backend describing any information to the user if needed",
        "resources": [
            {
                "title": "Resource 1 title",
                "download_url": "https://open.canada.ca/data/dataset/id_7_dataset_1.csv",
                "data_format": "csv",
                "languages": ["fr"],
            }
        ],
    },
]

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
                                                    # style={"width": "100%"},
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
    response_final = format_responses(temp_res)

    user_text = split_text(text)
    user_msg = [
        html.P(user, style={"text-align": "right", "margin": "1px"})
        for user in user_text
    ]

    if history:
        # order reversed so new lines always appear at the bottom in combiantion with CSS
        return (
            response_final
            + ["ComradeChat Bot:"]
            + user_msg
            + [html.Hr(style={"width": "100%"})]
            + history,
            "",
        )
    return response_final + ["ComradeChat Bot:"] + user_msg, ""


# run Dash app
if __name__ == "__main__":
    app.run_server()
