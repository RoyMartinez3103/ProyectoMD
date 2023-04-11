#Se importan las bibliotecas necesarias
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

from metodos import EDA

#Se inicializa la app
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR], suppress_callback_exceptions=True)

#Aspecto de la aplicación
app.title = "DataMinerX"

AspectStyle = {
    "margin-left":"5rem",
    "margin-right":"1rem",
}

title=dbc.Row([
            dbc.Col(    
                html.H1('DataMinerX'),
            width={'offset':5}
            )
]
)

    #Presentación de métodos
home = dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(src="https://www.mprj.mp.br/documents/20184/1517824/gif-grafico.gif", top=True),
                            dbc.CardBody(
                                [
                                    html.H4("Análisis Exploratorio de Datos (EDA)"),
                                    html.P(
                                        "Breve descripción"
                                        "----",
                                    ),
                                    dbc.Button("Realizar EDA a mis datos", color="primary", href="/EDA"),
                                ]
                            ),
                        ],
                        style={"width": "18rem"},
                    )
                ) ,

                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(src="https://matthewdeakos.me/wp-content/uploads/2018/02/ezgif.com-crop-4.gif"),
                            dbc.CardBody(
                                [
                                    html.H4("Análisis de Componentes Principales (PCA)"),
                                    html.P(
                                        "Breve descripción"
                                        "----",
                                    ),
                                    dbc.Button("Realizar PCA a mis datos", color="primary", href="/PCA"),
                                ]
                            ),
                        ],
                        style={"width": "18rem"},
                    )
                )
            ]
)

aspect = html.Div(id="aspecto", style=AspectStyle)

app.layout=html.Div([dcc.Location(id="url"),aspect, title, home])

@app.callback(Output('aspecto','children'),[Input('url','pathname')])
def page_content(pathname):
     if(pathname == "/EDA"):
         return EDA.layout
     elif (pathname=="/PCA"):
         return html.Div(
         [
             html.H1("404: Not found"),
             html.Hr(),
             html.P(f"The pathname {pathname} was not recognised..."),
         ],
         )

#Corre la aplicacion
if __name__ == '__main__':
    app.run_server(debug=True)