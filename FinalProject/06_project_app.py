import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

municipios_df = pd.read_csv('municipios_consolidados.csv' ) #, parse_dates=['Entry time'])
pqrs_df = pd.read_csv('pqrs_consolidados_30-nov.csv' ) 
pqrs_df['ANIO'] = pqrs_df['ANIO'].astype(str)

#df['YearMonth'] = pd.to_datetime(df['Entry time'].map(lambda x: x.strftime('%Y')))

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/uditagarwal/pen/oNvwKNP.css', 'https://codepen.io/uditagarwal/pen/YzKbqyV.css'])


app.layout = html.Div(children=[
    html.Div(
            children=[
                html.H1(children="Salud en Colombia", className='h1-title'),
            ],
            className='study-browser-banner row'
    ),
    html.Div(
        className="row app-body",
        children=[
            
            html.Div(
                className="padding row",
                children=[
                    html.Div(className="three columns ", 
                        children=[
                            html.H3("Parámetros:"),
                            html.Div(
                                className="card",
                                children=[
                                    html.H6("Período:"),
                                    dcc.Dropdown(
                                        id='anio-dropdown',
                                        options=[
                                            {'label': 'Todos', 'value': 'todos'},
                                            {'label': '2017', 'value': '2017'},
                                            {'label': '2018', 'value': '2018'},
                                            {'label': '2019', 'value': '2019'}
                                        ],
                                        multi=True,
                                        placeholder="Seleccione un año",
                                    ),
                                    html.H6("Departamento:"),
                                    dcc.Dropdown(
                                        id='departamento-dropdown',
                                        options=[
                                            {'label': i, 'value': i} for i in municipios_df['DEPARTAMENTO'].unique()
                                        ],
                                    ),
                                    html.H6("Municipio:"),
                                    dcc.Dropdown(
                                        id='municipio-dropdown',
                                        options=[
                                        ],
                                    ),
                                    html.H6("Institución:"),
                                    dcc.Dropdown(
                                        id='institucion-dropdown',
                                        options=[
                                        ],
                                    )
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        className="six columns",
                        children=[
                            html.H3("Top 10"),
                            html.H6("Variable:"),
                            dcc.Dropdown(
                                id='variable-tabla-dropdown',
                                options=[
                                    {'label': 'Alto costo', 'value': 'ALTO_COSTO'},
                                    {'label': 'Canal', 'value': 'PQR_CANAL'},
                                    {'label': 'Edad', 'value': 'AFEC_EDADR'},
                                    {'label': 'Entidad', 'value': 'ENT_NOMBRE'},
                                    {'label': 'Estado PQRS', 'value': 'PQR_ESTADO'},
                                    {'label': 'Género', 'value': 'AFEC_GENERO'},
                                    {'label': 'Grupo étnico', 'value': 'AFEC_GETNICO'},
                                    {'label': 'Macromotivo', 'value': 'MACROMOTIVO'},
                                    {'label': 'Motivo específico', 'value': 'MOTIVO_ESPECIFICO'},
                                    {'label': 'Motivo general', 'value': 'MOTIVO_GENERAL'},
                                    {'label': 'Nivel educativo', 'value': 'AFEC_EDUC'},
                                    {'label': 'Parentesco', 'value': 'AFEC_PARENTESCO'},
                                    {'label': 'Patología', 'value': 'PATOLOGIA_1'},
                                    {'label': 'Población Especial', 'value': 'AFEC_POBESPECIAL'},
                                    {'label': 'Régimen de afiliación', 'value': 'AFEC_REGAFILIACION'},
                                    {'label': 'Riesgo de vida', 'value': 'RIESGO_VIDA'},
                                    {'label': 'Tipo de persona', 'value': 'AFEC_TIPOPER'},
                                    {'label': 'Tipo de petición', 'value': 'PQR_TIPOPETICION'},
                                    {'label': 'Tipo patología', 'value': 'PATOLOGIA_TIPO'},
                                    {'label': 'Usuario', 'value': 'AFEC_ID'}

                                ],
                            ),
                            html.H6("Cantidades:"),
                            dcc.RadioItems(
                                id="absolute-radiobtn",
                                options=[
                                    {'label': 'Ambos', 'value': '1'},
                                    {'label': 'Absolutos', 'value': '2'},
                                    {'label': 'Porcentajes', 'value': '3'}
                                ],
                                value='1',
                                labelStyle={'display': 'inline-block'}
                            ),    
                            dash_table.DataTable(
                                id='top10-table',
                                columns=[
                                    
                                ],
                                #style_cell={'width': '50px'},
                                style_table={
                                    'maxHeight': '450px',
                                    'overflowY': 'scroll',
                                    'overflowX': 'scroll'
                                }
                            )
                        ]
                    ),
                    html.Div(
                        className="three columns",
                        children = [
                            
                            html.H3("Top 10")
                        ]
                    )
                ]
            ),
            # Comparación 
            html.Div(
                className="padding row",
                children=[
                    html.Div(
                        className="six columns",
                        children=[
                            html.Div(className="padding row",
                                children=[
                                html.Div(className="three columns",
                                    children=[
                                    html.H3("Comparación por municipio"),
                                    html.H6("Departamento:"),
                                    dcc.Dropdown(
                                        id='comparacion-departamento-dropdown',
                                        options=[
                                            {'label': i, 'value': i} for i in municipios_df['DEPARTAMENTO'].unique()
                                        ],
                                    ),
                                    html.H6("Municipio:"),
                                    dcc.Dropdown(
                                        id='comparacion-municipio-dropdown',
                                        options=[
                                        ],
                                    ),
                                    html.H6("Institución:"),
                                    dcc.Dropdown(
                                        id='comparacion-institucion-dropdown',
                                        options=[
                                        ],
                                    ),
                                    html.P("Gráfica de municipio 1")
                                ])
                            ]),
                            html.Div(className="padding row",
                                children=[
                                html.Div(className="three columns",
                                    children=[
                                    html.H3("Comparación por municipio"),
                                    html.P("Gráfica de municipio 2")
                                ])
                            ])
                            
                        ]
                    ),
                    html.Div(
                        className="six columns",
                        children=[
                            html.H3("Comparación por variables"),
                            html.P("Gráfica de municipio 1")
                        ]
                    )
                ]
            )
        ]
    )        
])

@app.callback(
    dash.dependencies.Output(component_id='municipio-dropdown', component_property='options'),
    [dash.dependencies.Input(component_id='departamento-dropdown', component_property='value')]
)
def update_municipio_dropdown(depto):
    #municipios = []
    
    #if depto != None:
    municipios = municipios_df[municipios_df['DEPARTAMENTO']==depto]['MUNICIPIO'].unique()
    
    municipios = [{'label': i, 'value': i} for i in municipios]
    return municipios


@app.callback(
    dash.dependencies.Output(component_id='institucion-dropdown', component_property='options'),
    [dash.dependencies.Input(component_id='departamento-dropdown', component_property='value'),
    dash.dependencies.Input(component_id='municipio-dropdown', component_property='value')]
)
def update_institucion_dropdown(depto, municipio):
    entidades = pqrs_df[(pqrs_df['AFEC_DPTO'] == depto) & (pqrs_df['AFEC_MPIO'] == municipio) &  (pqrs_df['ENT_NOMBRE'].notna())]['ENT_NOMBRE'].unique()
    
    print(entidades)
    entidades = [{'label': i, 'value': i} for i in entidades]
    return entidades

@app.callback(
    [
        dash.dependencies.Output(component_id='top10-table', component_property='data'),
        dash.dependencies.Output(component_id='top10-table', component_property='columns')
    ],   
    [
        dash.dependencies.Input(component_id='variable-tabla-dropdown', component_property='value'),
        dash.dependencies.Input(component_id='departamento-dropdown', component_property='value'),
        dash.dependencies.Input(component_id='municipio-dropdown', component_property='value'),
        dash.dependencies.Input(component_id='absolute-radiobtn', component_property='value')
    ]
)
def update_top10_table(variableInteres, depto, municipio, absolute_value):
    
    print("CHECKS!!!")
    print(absolute_value)
    columnas = []
    if absolute_value == '1':
        columnas = [variableInteres, '2017', '2018', '2019', '2017_PORC', '2018_PORC', '2019_PORC', '2018_2017_PORC', '2019_2018_PORC']
    elif absolute_value == '2':
        columnas = [variableInteres, '2017', '2018', '2019', '2018_2017_PORC', '2019_2018_PORC']
    else:
        columnas = [variableInteres, '2017_PORC', '2018_PORC', '2019_PORC', '2018_2017_PORC', '2019_2018_PORC']
    

    filtroTotal = np.ones((pqrs_df.shape[0], 1), dtype = bool).reshape(-1)
    filtroDepto = np.ones((pqrs_df.shape[0], 1), dtype = bool).reshape(-1)
    filtroMunicipio = np.ones((pqrs_df.shape[0], 1), dtype = bool).reshape(-1)
    
    if depto != None:
        filtroDepto = (pqrs_df['AFEC_DPTO'] == depto)

    if municipio != None:
        filtroMunicipio = (pqrs_df['AFEC_MPIO'] == municipio)
    
    if variableInteres == None:
        variableInteres = 'RIESGO_VIDA'


    filtroTotal = (filtroTotal & filtroDepto) & filtroMunicipio

    pqrsFiltrado = pqrs_df[filtroTotal]

    dff = consolidadoAnio(variableInteres, pqrsFiltrado).head(10)
    #dff = dff[columnas]
    return dff.to_dict('records'), [{'id': p, 'name': p} for p in dff.columns]



def consolidadoAnio(campo, datos_df, porcentajes=True, cambios=True):
  campos = ['ANIO']
  campos.append(campo)
  consolidado_anio_df = pd.DataFrame(datos_df.groupby(by=campos)['MES'].count()).reset_index()
  consolidado_anio_df = consolidado_anio_df.pivot(index=campo,columns='ANIO',values='MES').reset_index()
  consolidado_anio_df = consolidado_anio_df.sort_values(by='2019',ascending=False)

  if porcentajes:
    consolidado_anio_df["2017_PORC"]  = consolidado_anio_df['2017'] / consolidado_anio_df['2017'].sum()
    consolidado_anio_df["2018_PORC"]  = consolidado_anio_df['2018'] / consolidado_anio_df['2018'].sum()
    consolidado_anio_df["2019_PORC"]  = consolidado_anio_df['2019'] / consolidado_anio_df['2019'].sum()

  if cambios:
    consolidado_anio_df["2018_2017_PORC"]  = consolidado_anio_df['2018'] / consolidado_anio_df['2017']
    consolidado_anio_df["2019_2018_PORC"]  = consolidado_anio_df['2019'] / consolidado_anio_df['2018']
    
  return consolidado_anio_df


if __name__ == "__main__":
    app.run_server(debug=True)