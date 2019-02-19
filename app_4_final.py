import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

import pandas as pd


def read_data():
    df = pd.read_csv('data.csv', index_col=0)
    df.set_index('ID', inplace=True)
    return df


def get_skill_options(df):
    skills = []
    for c in df.columns:
        if df.dtypes[c] == float:
            skills.append(c)
    skills.sort()
    return [{'label': x, 'value': x} for x in skills]


def get_club_options(df):
    idx = df['Club'].apply(lambda x: isinstance(x, str))
    clubs = list(df.loc[idx, 'Club'].unique())
    return [{'label': x, 'value': x} for x in clubs]


df = read_data()

skill_options = get_skill_options(df)
skill_x_default = 'Dribbling'
skill_y_default = 'Finishing'

club_options = get_club_options(df)
club_default = 'FC Barcelona'

photo_default = df['Photo'].iloc[0]
logo_default = df['Club Logo'].iloc[0]
name_default = df['Name'].iloc[0]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            html.Img(
                id="fifa-image", 
                src="https://assets1.ignimgs.com/2018/06/09/fifa-19---button-1528581836001.jpg",
                height=200,
                width=200,
            ),
        ], style={'float': 'left'}),
        html.Div(children=[
            html.Div('Select one or multiple clubs', style={'fontSize': 20}),
            dcc.Dropdown(
                id='club-dropdown',
                options=club_options,
                value=club_default,
                multi=True
            ),
            html.Div('Select skill for x axis', style={'fontSize': 20}),
            dcc.Dropdown(
                id='skill-x-dropdown',
                options=skill_options,
                value=skill_x_default,
                style={'width': '50%'}
            ),
            html.Div('Select skill for y axis', style={'fontSize': 20}),
            dcc.Dropdown(
                id='skill-y-dropdown',
                options=skill_options,
                value=skill_y_default,
                style={'width': '50%'}
            ),
        ], style={'margin-left': 250, 'margin-right': 200})
    ], className="row"),
    html.Div(children=[
        html.Div(children=[
            html.Div(id="player-name", className="row"),
            html.Div(children=[
                html.Img(id="player-photo", width=100), #height=70),
                html.Img(id="club-logo"),
            ])
        ], style={'float': 'left', 'margin-top': 100, 'margin-left': 50}),
        dcc.Graph(id="scatter-plot", style={'margin-left': 200, 'margin-right': 200})
    ])
])

@app.callback(
    Output(component_id='scatter-plot', component_property='figure'),
    [Input(component_id='club-dropdown', component_property='value'),
    Input(component_id='skill-x-dropdown', component_property='value'),
    Input(component_id='skill-y-dropdown', component_property='value')]
)
def update_scatter_plot(clubs, skill_x, skill_y):
    if not isinstance(clubs, list):
        clubs = [clubs]
    layout = go.Layout(
        xaxis={'title': skill_x},
        yaxis={'title': skill_y},
        hovermode='closest',
    )
    data = []
    for club in clubs:
        idx = (df['Club'] == club)
        data.append(go.Scatter(
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=club,
            x=df.loc[idx, skill_x],
            y=df.loc[idx, skill_y],
            text=df.index[idx],
            hoverinfo='none',
        ))
    return go.Figure(data=data, layout=layout)


@app.callback(
    Output(component_id='player-photo', component_property='src'),
    [Input(component_id='scatter-plot', component_property='hoverData')]
)
def update_player_photo(hoverData):
    if not hoverData:
        return photo_default
    else:
        player_id = int(hoverData['points'][0]['text'])
        url = df.loc[player_id, 'Photo']
        return url

@app.callback(
    Output(component_id='club-logo', component_property='src'),
    [Input(component_id='scatter-plot', component_property='hoverData')]
)
def update_club_logo(hoverData):
    if not hoverData:
        return logo_default
    else:
        player_id = int(hoverData['points'][0]['text'])
        url = df.loc[player_id, 'Club Logo']
        return url

@app.callback(
    Output(component_id='player-name', component_property='children'),
    [Input(component_id='scatter-plot', component_property='hoverData')]
)
def update_player_name(hoverData):
    if not hoverData:
        return name_default
    else:
        player_id = int(hoverData['points'][0]['text'])
        url = df.loc[player_id, 'Name']
        return url


if __name__ == '__main__':
    app.run_server(debug=True)

