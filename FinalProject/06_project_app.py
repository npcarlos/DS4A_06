import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


from urllib.request import urlopen
import plotly.graph_objects as go
import json
import geopandas as gpd
import geoplot as gplt

import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from wordcloud import WordCloud



# #######################################################
#           CARGA DE DATOS
# #######################################################


municipios_df = pd.read_csv('municipios_consolidados.csv' ) 
pqrs_df = pd.read_csv('pqrs_consolidados_30-nov.csv' ) 
pqrs_df['ANIO'] = pqrs_df['ANIO'].astype(str)



with open('Colombia.geo.json') as col:
    geod = json.load(col)

with open('mun.geojson', encoding="utf8") as col:
    mung = json.load(col)

c=1
for i in geod['features']:
    i['id']=int(i['properties']['DPTO'])

mung_df = gpd.read_file('mun.geojson')

m_geo_df = mung_df[['ID_ESPACIA', 'AREA_OFICI', 'ENTIDAD_TE', 'geometry']]
m_geo_df['LATITUD'] = m_geo_df['geometry'].y
m_geo_df['LONGITUD'] = m_geo_df['geometry'].x

municipios_df2 = pd.read_csv('mun_.csv')
departamentos_df = municipios_df2.groupby(['COD_DEPTO','DEPARTAMENTO']).sum().reset_index()






# #######################################################
#           CREACIÓN DEL APP
# #######################################################

app = dash.Dash(__name__, external_stylesheets=["css/bootstrap.css", dbc.themes.GRID, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"]) #, 'https://codepen.io/uditagarwal/pen/oNvwKNP.css', 'https://codepen.io/uditagarwal/pen/YzKbqyV.css'])




# #######################################################
#           NAV BAR
# #######################################################


navbar = dbc.NavbarSimple(
    [
        #dbc.Nav(html.Img(src=app.get_asset_url("img/logo-peq.png"), height="60px"), horizontal="start", no_gutters=True),
        #dbc.NavbarBrand("Salud en Colombia [2017 - 2019 (Oct)]", className="ml-2"),
        dbc.Row(
            [
                dbc.Col(html.Img(src=app.get_asset_url("img/logo-peq.png"), height="30px")),
                dbc.Col(dbc.NavbarBrand("Salud en Colombia [2017 - 2019 (Oct)]", className="ml-2")),
            ],
            align="center",
            no_gutters=True,
            style={
                'padding-right' : "30px"
            }
        ),
        dbc.NavItem(dbc.NavLink([
                        html.P("Geográfico"),
                        html.I(className='fa fa-globe'),
                    ], href="#", style={'text-align' : "center"})),
        dbc.NavItem(dbc.NavLink([
                        html.P("Usuarios"),
                        html.I(className='fa fa-users'),
                    ], href="usuario", style={'text-align' : "center"})),
        dbc.NavItem(dbc.NavLink([
                        html.P("Sugeridos"),
                        html.I(className='fa fa-chart'),
                    ], href="#", style={'text-align' : "center"})),
        dbc.NavItem(dbc.Button(
            [
                html.I(className='fa fa-gear'),
            ],
            id="open-centered"
        )),
        dbc.NavItem(dbc.Button(
            [
                html.I(className='fa fa-info'),
            ],
            id="open-info"
        )),
        dbc.NavbarToggler(id="navbar-toggler"),
        #dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    #color="dark",
    color="primary",
    dark=True,
    sticky="top",
)
"""

dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Entry 1"),
                dbc.DropdownMenuItem(
                    [
                        html.I(className='fa fa-gear'),
                        html.P("Informes sugeridos")
                    ]
                ),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem(
                    [
                        html.I(className='fa fa-info-circle'),
                        html.P("Info")
                    ]
                ),
            ],
        ),

navbar = dbc.NavbarSimple(
    children=[
        dbc.Button(
            [
                "Parámetros ",
                html.I(className='fa fa-gear'),
            ],
            id="open-centered"
        ),
        dbc.NavItem(dbc.NavLink("Link", href="#")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Entry 1"),
                dbc.DropdownMenuItem("Entry 2"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Entry 3"),
            ],
        ),
    ],
    style={
        'background': '#108de4',
        'color' : 'white'
    },
    brand="Salud en Colombia [2017 - 2019 (Oct)]",
    brand_href="#",
    sticky="top",
)
"""




# #######################################################
#           MODAL DE PARÁMETROS
# #######################################################


tab1_content = dbc.Card(
    dbc.CardBody(
        [   
            #"""
            #html.H6("Período:"),
            
            #dcc.Dropdown(
            #    id='anio-dropdown',
            #    options=[
            #        {'label': 'Todos', 'value': 'todos'},
            #        {'label': '2017', 'value': '2017'},
            #        {'label': '2018', 'value': '2018'},
            #        {'label': '2019', 'value': '2019'}
            #    ],
            #    multi=True,
            #    placeholder="Seleccione un año",
            #),
            #"""
            html.H6("Departamento:"),
            dcc.Dropdown(
                id='departamento-dropdown',
                options=[
                    {'label': i, 'value': i} for i in municipios_df['DEPARTAMENTO'].unique()
                ],
                placeholder="Seleccione un departamento",
            ),
            html.H6("Municipio:"),
            dcc.Dropdown(
                id='municipio-dropdown',
                options=[
                ],
                placeholder="Seleccione un municipio",
            ),
            html.H6("Institución:"),
            dcc.Dropdown(
                id='institucion-dropdown',
                options=[
                ],
                placeholder="Seleccione una institución",
            )
        ]
    ),
    #className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Cantidades:"),
            dcc.Dropdown(
                id='filtro-cantidades-dropdown',
                options=[
                    {'label': 'Absolutos', 'value': 'abs'},
                    {'label': 'Porcentajes', 'value': 'porc'},
                    {'label': 'Variaciones anuales', 'value': 'variaciones'}
                ],
                placeholder="Seleccione una institución",
                multi=True
            ),   
            html.H6("Tipo de persona:"),
            dcc.RadioItems(
                id="tipo-persona-radiobtn",
                options=[
                    {'label': 'Ambos', 'value': '1'},
                    {'label': 'Jurídica', 'value': 'JURIDICA'},
                    {'label': 'Natural', 'value': 'NATURAL'}
                ],
                value='1',
                labelStyle={'display': 'inline-block', 'padding':"15px"}
            ),   
            html.H6("Tipo de persona:"),
            dcc.RadioItems(
                id="mejores-peores-radiobtn",
                options=[
                    {'label': 'Primeros 10', 'value': 'top'},
                    {'label': 'Últimos 10', 'value': 'bottom'}
                ],
                value='top',
                labelStyle={'display': 'inline-block', 'padding':"15px"}
            )
        ]
    ),
    #className="mt-3",
)





# #######################################################
#           CONTENIDO
# #######################################################

body = dbc.Container(
    [
        


        # #######################################################
        #           TÍTULO
        # #######################################################

        dbc.Row(
            [
                html.H1(
                    "Análisis del Sistema de Salud en Colombia",
                    
                )
            ],
            style={
                'textAlign': 'center',
                'padding-left': '60px',
                'padding-top': '50px',
                'padding-bottom': '50px'
            }
        ),
        


        # #######################################################
        #           INTRODUCCIÓN
        # #######################################################

        dbc.Row(
            [
                html.P(
                        """\
Explore alguna de las variables disponibles acerca de los PQRS que se han presentado en todo el país ante la Superintendencia Nacional de Salud desde 2017 a 2019 (Oct)."""
                        ),
            ]
        ),
        

        # #######################################################
        #           PANEL PRINCIPAL  - PRIMERA FILA
        # #######################################################

        dbc.Row(
            [
                dbc.Col(
                    [
                        

                        # #######################################################
                        #           COLUMNA IZQUIERDA
                        # #######################################################

                        html.H2(
                            children=
                            [
                                html.I(className='fa fa-trophy'),
                                " Top 10"
                            ],
                            id="titulo_top_10"
                        ),
                        dbc.Row(
                            [
                                html.P(
                                    children=[
                                        "Variable de interés: ",
                                        dcc.Dropdown(
                                            id='variable-tabla-dropdown',
                                            placeholder="Variables de análisis",
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

                                            ]
                                        )
                                    ]
                                ),
                                dbc.Modal(
                                            [
                                                dbc.ModalHeader("Parámetros"),
                                                dbc.ModalBody(
                                                    dbc.Tabs(
                                                        [
                                                            dbc.Tab(tab1_content, label="Geográficos"),
                                                            dbc.Tab(tab2_content, label="Filtros")
                                                        ]
                                                    )
                                                ),
                                                dbc.ModalFooter(
                                                    dbc.Button(
                                                        "Close", id="close-centered", className="ml-auto"
                                                    )
                                                ),
                                            ],
                                            id="modal-centered",
                                            centered=True,
                                )
                            ]
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
                        ),
                        #html.H3(
                        #    children=
                        #    [
                        #        html.I(className='fa chart-bar'),
                        #        " Gráfico"
                        #    ]
                        #),
                        dcc.Graph(
                            figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]},
                            id="grafico-principal"
                        )
                    ],
                    md=8,
                ),
                dbc.Col(
                    [

                        # #######################################################
                        #           COLUMNA DERECHA
                        # #######################################################

                        html.H2(
                            children=
                            [
                                html.I(className='fa fa-map-marker'),
                                " ¿Dónde?"
                            ]
                        ),
                        dcc.Graph(id="mapa-principal"),
                        
                    ]
                ),
            ]
        ),
        

        # #######################################################
        #           TÍTULO COMPARACIÓN
        # #######################################################

        dbc.Row(
            [
                html.H1(
                    "¿Qué tal si comparamos?",
                    style={
                        'textAlign': 'center',
                        'padding-left': '200px',
                        'padding-top': '50px',
                        'padding-bottom': '50px'
                    }
                )
            ]
        ),
        

        # #######################################################
        #           COMPARACIÓN
        # #######################################################

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Otro "),
                        html.P(
                            """\
Escoge otro departamento para comparar"""
                        ),
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
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        html.H2("Graph"),
                        dcc.Graph(
                            figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]}
                        ),
                    ]
                ),
            ]
        ),
        

        # #######################################################
        #           Usuarios
        # #######################################################
        dbc.Row(
            [
                html.H1(
                    "Análisis por usuario",
                    style={
                        'textAlign': 'center',
                        'padding-left': '200px',
                        'padding-top': '50px',
                        'padding-bottom': '50px'
                    },
                    id="usuario"
                ),
                dcc.Graph(id="wordcloudfig"),
            ]
        ),
    ],
    className="mt-4",
)
"""
html.Div(children=[
    html.Div(
            children=[
                html.H1(children="Salud en Colombia", className='h1-title'),
                dbc.Button("Open", id="open-centered"),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Parámetros"),
                        dbc.ModalBody(
                            dbc.Tabs(
                                [
                                    dbc.Tab(tab1_content, label="Geográficos"),
                                    dbc.Tab(tab2_content, label="Filtros")
                                ]
                            )
                        ),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Close", id="close-centered", className="ml-auto"
                            )
                        ),
                    ],
                    id="modal-centered",
                    centered=True,
                )
            ],
            className='study-browser-banner row'
    ),
    html.Div(
        className="row app-body",
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                className="padding",
                                children=[
                                    html.Div(
                                        #className="six columns",
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
                                        #className="three columns",
                                        children = [
                                            
                                            html.H3("Top 10")
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                    
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            # Comparación 
                            html.Div(
                                className="padding",
                                children=[
                                    html.Div(
                                        #className="six columns",
                                        children=[
                                            html.Div(
                                                #className="padding row",
                                                children=[
                                                html.Div(
                                                    #className="three columns",
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
                                            html.Div(
                                                #className="padding row",
                                                children=[
                                                html.Div(
                                                    #className="three columns",
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
                ]
            )
        ]
    )        
])
"""

# #######################################################
#          APP LAYOUT
# #######################################################

app.layout = html.Div([navbar, body])

#
# Abre la ventana de parámetros
# 
 
@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open




# #######################################################
#           CALL BACK  - DROPDOWN  DE PARÁMETROS
# #######################################################


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
    dash.dependencies.Output(component_id='comparacion-municipio-dropdown', component_property='options'),
    [dash.dependencies.Input(component_id='comparacion-departamento-dropdown', component_property='value')]
)
def update_municipio_dropdown(depto):
    #municipios = []
    
    #if depto != None:
    municipios = municipios_df[municipios_df['DEPARTAMENTO']==depto]['MUNICIPIO'].unique()
    
    municipios = [{'label': i, 'value': i} for i in municipios]
    return municipios


@app.callback(
    dash.dependencies.Output(component_id='comparacion-institucion-dropdown', component_property='options'),
    [dash.dependencies.Input(component_id='comparacion-departamento-dropdown', component_property='value'),
    dash.dependencies.Input(component_id='comparacion-municipio-dropdown', component_property='value')]
)
def update_institucion_dropdown(depto, municipio):
    entidades = pqrs_df[(pqrs_df['AFEC_DPTO'] == depto) & (pqrs_df['AFEC_MPIO'] == municipio) &  (pqrs_df['ENT_NOMBRE'].notna())]['ENT_NOMBRE'].unique()
    
    print(entidades)
    entidades = [{'label': i, 'value': i} for i in entidades]
    return entidades


# #######################################################
#           CALL BACK  - TABLA PRINCIPAL
# #######################################################


@app.callback(
    [
        dash.dependencies.Output(component_id='top10-table', component_property='data'),
        dash.dependencies.Output(component_id='top10-table', component_property='columns'),
        #dash.dependencies.Output("grafico-principal", "figure")
    ],   
    [
        dash.dependencies.Input(component_id='variable-tabla-dropdown', component_property='value'),
        dash.dependencies.Input(component_id='departamento-dropdown', component_property='value'),
        dash.dependencies.Input(component_id='municipio-dropdown', component_property='value'),
        dash.dependencies.Input(component_id='filtro-cantidades-dropdown', component_property='value'),
        dash.dependencies.Input(component_id='tipo-persona-radiobtn', component_property='value')    ,
        dash.dependencies.Input(component_id='mejores-peores-radiobtn', component_property='value')        
    ]
)
def update_top10_table(variableInteres, depto, municipio, cantidades, tipoPersona, mejoresPeores):
    
    filtroTotal = np.ones((pqrs_df.shape[0], 1), dtype = bool).reshape(-1)
    
    if depto != None:
        filtroTotal = filtroTotal & (pqrs_df['AFEC_DPTO'] == depto)

    if municipio != None:
        filtroTotal = filtroTotal & (pqrs_df['AFEC_MPIO'] == municipio)
    
    if variableInteres == None:
        variableInteres = 'RIESGO_VIDA'

    columnas = [variableInteres]


    if ((cantidades == None) or ('abs' in cantidades) ):
        columnas += ['2017', '2018', '2019']
    
    if ((cantidades == None) or ('porc' in cantidades) ):
        columnas += ['2017_PORC', '2018_PORC', '2019_PORC']
    
    if ((cantidades == None) or ('variaciones' in cantidades) ):
        columnas += ['2017_2018_PORC', '2018_2019_PORC']
    
    if tipoPersona != '1':
        filtroTotal = filtroTotal & (pqrs_df['AFEC_TIPOPER'] == tipoPersona)
    
    pqrsFiltrado = pqrs_df[filtroTotal]

    # Tabla
    dff = consolidadoAnio(variableInteres, pqrsFiltrado)
    
    if mejoresPeores == "bottom":
        dff = dff.tail(10)
    else:
        dff = dff.head(10)

    dff_tabla = dff[columnas]

    # Gráfico
    #g_df = consolidadoAnio('AFEC_PARENTESCO', datos_df=pqrs_df[(pqrs_df['AFEC_PARENTESCO'] != 'NOMBRE PROPIO')]).sort_values(by=2019,ascending=False).head(15)
    #g_df = dff
    #g_df.columns = ['AFEC_PARENTESCO',	'2017_total',	'2018_total',	'2019_total',	'2017',	'2018',	'2019',	'2018_2017_PORC',	'2019_2018_PORC']
    g_df = pd.melt(dff, id_vars=[variableInteres], value_vars=['2017','2018','2019'], value_name="Porcentaje_anual")
    g_df.columns = [variableInteres, "Año", "valor"]

    f, ax = plt.subplots(figsize=(10, 10))
    ax = sns.barplot(x="valor", y=variableInteres, data=g_df, hue="Año")

    return dff_tabla.to_dict('records'), [{'id': p, 'name': p} for p in dff_tabla.columns]#, ax



def consolidadoAnio(campo, datos_df, porcentajes=True, cambios=True):
  campos = ['ANIO']
  campos.append(campo)
  consolidado_anio_df = pd.DataFrame(datos_df.groupby(by=campos)['MES'].count()).reset_index()
  consolidado_anio_df = consolidado_anio_df.pivot(index=campo,columns='ANIO',values='MES').reset_index()
  consolidado_anio_df = consolidado_anio_df.sort_values(by='2019',ascending=False)

  if porcentajes:
    consolidado_anio_df["2017_PORC"]  = round(100 * consolidado_anio_df['2017'] / consolidado_anio_df['2017'].sum(), 2)
    consolidado_anio_df["2018_PORC"]  = round(100 * consolidado_anio_df['2018'] / consolidado_anio_df['2018'].sum(), 2)
    consolidado_anio_df["2019_PORC"]  = round(100 * consolidado_anio_df['2019'] / consolidado_anio_df['2019'].sum(), 2)

  if cambios:
    consolidado_anio_df["2017_2018_PORC"]  = round((100 * consolidado_anio_df['2018'] / consolidado_anio_df['2017']) - 100, 2) 
    consolidado_anio_df["2018_2019_PORC"]  = round((100 * consolidado_anio_df['2019'] / consolidado_anio_df['2018']) - 100, 2)
    
  return consolidado_anio_df



# #######################################################
#           CALL BACK  - TÍTULO TOP 10 
# #######################################################


@app.callback(
    [
        dash.dependencies.Output("titulo_top_10", "children")#,
        #dash.dependencies.Output("wordcloudfig", "figure")
    ],
    [
        dash.dependencies.Input(component_id='departamento-dropdown', component_property='value'),
        dash.dependencies.Input(component_id='municipio-dropdown', component_property='value'),
        dash.dependencies.Input(component_id='mejores-peores-radiobtn', component_property='value')
    ]
)
def update_titulo(departamentoSeleccionado, municipioSeleccionado, mejoresPeores):
    parte = " Primeros"
    icono = 'fa fa-trophy'
    if mejoresPeores == "bottom":
        parte = " Últimos"
        icono = 'fa fa-thumbs-down'
    

    titulo = parte + " 10 - Nacional"
    
    if departamentoSeleccionado != None:
        titulo = parte + " 10 - " + departamentoSeleccionado
        if municipioSeleccionado != None:
            titulo = parte + " 10 - " + municipioSeleccionado + " (" + departamentoSeleccionado + ")"

    paciente = pqrs_df[pqrs_df['AFEC_ID'] == 518513]
    causas = paciente[['MOTIVO_ESPECIFICO', 'PATOLOGIA_1', 'PATOLOGIA_TIPO', 'CIE_10']]
    causas = causas["MOTIVO_ESPECIFICO"].astype(str) +" "+ causas["PATOLOGIA_1"] +" "+ causas["PATOLOGIA_TIPO"] +" "+ causas["CIE_10"]
    causas = causas[~causas.isnull()]
    word_cloud_text = ''.join(causas.tolist())
    wordcloud = WordCloud(max_font_size=100, max_words=100, background_color="white",\
                            scale = 10,width=800, height=400).generate(word_cloud_text)
                            
    fig = plt.figure(figsize = (15, 30))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    return [html.I(className=icono), titulo] #, fig


# #######################################################
#           CALL BACK  - MAPA
# #######################################################


@app.callback(
    dash.dependencies.Output("mapa-principal", "figure"),
    [
        dash.dependencies.Input(component_id='departamento-dropdown', component_property='value'),
        dash.dependencies.Input(component_id='municipio-dropdown', component_property='value')
    ]
)
def update_mapa_principal(departamentoSeleccionado, municipioSeleccionado):
    
    capas = []
    departamentosSeleccionados_df = departamentos_df

    if departamentoSeleccionado != None:
        departamentosSeleccionados_df = departamentos_df[departamentos_df['DEPARTAMENTO'] == departamentoSeleccionado]
        codDeptoSeleccionado = departamentosSeleccionados_df['COD_DEPTO'].iloc[0]
        
        listaMunicipios = municipios_df2[municipios_df2['COD_DEPTO'] == codDeptoSeleccionado]
        listaMunicipios = listaMunicipios['COD_MUNICIPIO'].values.reshape(-1)
        print(listaMunicipios)
        print(listaMunicipios.shape)
        muncipiosEnDepto_df2 = m_geo_df[m_geo_df['ID_ESPACIA'].isin(listaMunicipios)]
        print("**** MUNICIPIOS*")
        print(muncipiosEnDepto_df2)
        muncipiosEnDepto_df = m_geo_df
        munpoint = go.Scattermapbox(
            lat = muncipiosEnDepto_df['LATITUD'],
            lon = muncipiosEnDepto_df['LONGITUD'],
            mode = 'markers',
            text = muncipiosEnDepto_df['ID_ESPACIA']
        )            
        

    g = go.Choroplethmapbox(geojson = geod,
                        locations = departamentosSeleccionados_df['COD_DEPTO'], z = departamentosSeleccionados_df['NUM_PQRS_2019'],
                        colorscale = "Viridis", zmin = 0, zmax = 12,
                        marker_opacity = 0.5, marker_line_width = 0, hovertext = departamentosSeleccionados_df['DEPARTAMENTO'])
    capas.append(g)

    if departamentoSeleccionado != None:
        capas.append(munpoint)


    lyt = go.Layout(mapbox_style = "carto-positron",
                mapbox_zoom = 3, mapbox_center = {"lat": 4, "lon": -72})
    
    
    
    fig = go.Figure(data = capas,layout = lyt)
    return fig


""" 
@app.callback(
    dash.dependencies.Output(component_id='comparacion-departamento-dropdown', component_property='value'),
    [dash.dependencies.Input(component_id='departamento-dropdown', component_property='value')]
)
def update_comparacion_depto_dropdown(depto):
    #municipios = []
    
    if depto == None:
    return municipios




 """

if __name__ == "__main__":
    app.run_server(debug=True)