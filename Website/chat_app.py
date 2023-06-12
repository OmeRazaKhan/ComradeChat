import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html

app = dash.Dash()

app.layout = html.Div([
    html.H1('ComradeChat', style={'text-align': 'center'}),
    html.Div([
        html.Div([
            html.Br(),
            html.Div(id='conversation',
                     style={'max-height': '500px', 'overflow-y': 'scroll', 'display': 'flex', 'flex-direction': 'column-reverse'}),
            html.Br(),
            html.Table([
                html.Tr([
                    # user text input
                    html.Td([dcc.Input(id='msg_input', placeholder='Type Here . . .', type='text', style={'width': '80%'})],
                            style={'width': '100%', 'valign': 'middle'}),
                    # send user text
                    html.Td([html.Button('Send', id='send_button', type='submit', style={'width': '100%'})],
                            style={'width': '100%', 'valign': 'middle'})
                ])
            ])],
            style={'margin': '0 auto'})],
        id='screen',
        style={'width': '500px', 'height': '500px', 'margin': '0 auto'})
])

# callback for when user sends a message
@app.callback(
    [
        Output('conversation', 'children'),
        Output('msg_input', 'value'),
    ],
    [
        Input('send_button', 'n_clicks'),
        State('conversation', 'children'),
        State('msg_input', 'value')
    ],
    prevent_initial_call=True
)
def process_message(n_clicks, history, text):
    # Put the text processing/response stuff here?
    
    # temporary place holder response
    response = ["This is response 1", "Here we have response number 2", "Here would be some 3rd response if there was one"]

    user_msg = [html.P(text, style={'text-align': 'right'})]
    response_msg = [html.P(html.I(res), style={'text-align': 'left'}) for res in response]
    
    if history:
        return response_msg + user_msg + [html.Hr(style={'width': '100%'})] + history, ''  # order reversed so new lines always appear at the bottom in combiantion with CSS
    return response_msg + user_msg, ''

# run Dash app
if __name__ == '__main__':
    app.run_server()