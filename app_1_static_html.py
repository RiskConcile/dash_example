import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.H1('First app'),
    html.Img(
        src="https://assets1.ignimgs.com/2018/06/09/fifa-19---button-1528581836001.jpg",
        width=200,
        height=200)
])

if __name__ == '__main__':
    app.run_server(debug=True)




