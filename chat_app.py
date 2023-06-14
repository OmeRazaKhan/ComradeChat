# Importing Packages
from dash import Dash, Input, Output, State, html
import dash_bootstrap_components as dbc

from api.api import API
from chat_app_util import format_responses

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder="assets")
api = API("resources/datasets.json")

app.layout = html.Div(
    [
        html.H1("ComradeChat", className="title"),
        html.Div(
            [
                html.Div(
                    [
                        html.Br(),
                        html.Div(id="conversation", className="conversation"),
                        html.Br(),
                        html.Table(
                            [
                                html.Tr(
                                    [
                                        html.Td(
                                            [
                                                dbc.Input(
                                                    id="msg_input",
                                                    placeholder="Type Here...",
                                                    type="text",
                                                    className="input",
                                                )
                                            ],
                                            className="input-bar",
                                        ),
                                        html.Td(
                                            [
                                                dbc.Button(
                                                    "Send",
                                                    id="send_button",
                                                    type="submit",
                                                    style={"width": "100%"},
                                                )
                                            ],
                                            className="input-bar",
                                        ),
                                    ]
                                )
                            ]
                        ),
                    ],
                    className="conversation-block",
                )
            ],
            id="screen",
            className="screen",
        ),
    ]
)


# callback for when user sends a message
@app.callback(
    [Output("conversation", "children"), Output("msg_input", "value")],
    [
        Input("send_button", "n_clicks"),
        State("conversation", "children"),
        State("msg_input", "value"),
    ],
    prevent_initial_call=True,
)
def process_message(n_clicks, history, text):
    response_final = format_responses(
        api.generate_response(text, maximum_num_responses=4)
    )
    user_msg = [html.P(text, className="user-msg")]
    response_final.reverse()
    response_final = [html.P(response_final, className="generated-msg")]

    if history:
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
