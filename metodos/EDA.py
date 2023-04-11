#Se importan las bibliotecas necesarias
import base64
import datetime
import io

import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dash, dcc, html, Input, Output, callback, State, dash_table
           # Para la manipulación y análisis de datos
#import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
import pandas as pd



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.VAPOR], suppress_callback_exceptions=True)

layout = html.Div([
        html.H1('Análisis Exploratorio de Datos (EDA)', style={'text-align': 'center'}),
        # dbc.Row(
        #     dbc.Col(    
        #         html.H1('Análisis Exploratorio de Datos (EDA)'),
        #     width={'offset':3}
        #     )
        # ),

    html.Div(
        [ 
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Suelta o ',
                    html.A('seleciona un archivo',href="#")
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '2px',
                    'borderStyle': 'solid',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Div(id='output-div'), #Guarda el segundo callback
            html.Div(id='output-datatable'), #Guarda la información del primer callback
        ]
    )
    ])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
            print(e)
            return html.Div([
                'Hubo un error al procesar el archivo'
            ])
    
    return html.Div([
        dbc.Alert("El archivo es: " + filename, color="info"),
        html.H3("Paso 1. Visualización de datos"),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=15,
            style_cell={'textAlign':'left'},
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },

        ),
        dcc.Store(id='stored-data', data=df.to_dict('records')),

        html.Hr(),  # horizontal line

])


@app.callback(Output('output-datatable', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


@app.callback(Output('output-div', 'children'),
              Input('submit-button','n_clicks'),
              State('stored-data','data'),
              State('xaxis-data','value'),
              State('yaxis-data', 'value'))
def make_graphs(n, data, x_data, y_data):
    if n is None:
        return dash.no_update
    else:
        bar_fig = px.bar(data, x=x_data, y=y_data)
        # print(data)
        return dcc.Graph(figure=bar_fig)







# #Se importan los datos
# dbc.Input(id="inputFile", type="file"),
# data = pd.read_csv("melb_data.csv")
# data

# #Estructura de los datos
# data.shape

#Corre la aplicacion
#if __name__ == '__main__':
 #   app.run_server(debug=True)