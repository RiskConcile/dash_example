import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1('First app'),
    html.Img(
        src="https://assets1.ignimgs.com/2018/06/09/fifa-19---button-1528581836001.jpg",
        width=200,
        height=200),
    dcc.Dropdown(
        id='club-dropdown',
        options=club_options,
        value=club_default,
        multi=True
    ),
    dcc.Dropdown(
        id='skill-x-dropdown',
        options=skill_options,
        value=skill_x_default,
    ),
    dcc.Dropdown(
        id='skill-y-dropdown',
        options=skill_options,
        value=skill_y_default,
    ),
    dcc.Graph(id='scatter-plot')
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
        ))
    return go.Figure(data=data, layout=layout)


if __name__ == '__main__':
    app.run_server(debug=True)




