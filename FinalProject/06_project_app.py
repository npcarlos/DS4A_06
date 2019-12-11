import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.tools as tls
import plotly.graph_objs

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


integrantes = ["Santiago Cuervo", "Ricardo Granados", "Héctor Jaramillo", "Carlos Navarrete", "Diego Rey", "Nicolás Arce"]
fuentesDeDatos = ["PQRS Superintendencia Nacional de Salud", "Ministerio de Hacienda", "Censo poblacional DANE 2015" ]

#municipios_df = pd.read_csv('municipios_consolidados.csv' ) 
pqrs_df = pd.read_csv('pqr_.csv' ) 
#pqrs_df = pd.read_csv('pqrs_consolidados_30-nov.csv' ) 

pqrs_df['ANIO'] = pqrs_df['ANIO'].astype(str)



with open('Colombia.geo.json') as col:
    geod = json.load(col)

with open('mun.geojson', encoding="utf8") as col:
    mung = json.load(col)

c=1
for i in geod['features']:
    i['id']=int(i['properties']['DPTO'])

mung_df = gpd.read_file('mun.geojson')

m_geo_df = mung_df[['COD_DEPTO', 'ID_ESPACIA', 'AREA_OFICI', 'ENTIDAD_TE', 'geometry']]
m_geo_df['COD_DEPTO'] = m_geo_df['COD_DEPTO'].astype(int)
m_geo_df['ID_ESPACIA'] = m_geo_df['ID_ESPACIA'].astype(int)
m_geo_df['LATITUD'] = m_geo_df['geometry'].y
m_geo_df['LONGITUD'] = m_geo_df['geometry'].x

municipios_df = pd.read_csv('mun_.csv')
municipios_df['COD_MUNICIPIO'] = municipios_df['COD_MUNICIPIO'].astype(int)
print(municipios_df.info())

#print(type(municipios_df['COD_MUNICIPIO']))
departamentos_df = municipios_df.groupby(['COD_DEPTO','DEPARTAMENTO']).sum().reset_index()

deptos_geo_df = gpd.read_file('geo_deptos.geojson')
deptos_geo_df['DPTO'] = deptos_geo_df['DPTO'].astype(int)

available_indicators = [
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
                dbc.Col(html.Img(src = app.get_asset_url("img/logo-peq.png"), height = "30px")),
                dbc.Col(dbc.NavbarBrand("Salud en Colombia [2017 - 2019 (Oct)]", className = "ml-2")),
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
                    ], href="#", style={'text-align' : "center"}, id='linkSugeridos')),
        dbc.NavItem(dbc.Button(
            [
                html.I(className='fa fa-check'),
            ],
            id="open-sugerencias"
        )),
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
    #sticky="top",
)


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
                    {'label': row[0], 'value': row[1]} for row in departamentos_df[['DEPARTAMENTO', 'COD_DEPTO']].values
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


#
# The goal is to change the parameters value according to the selected suggested analysis

sugerencias = [
        "Morbilidad per cápita VS. PIB per cápita",
        "Morbilidad per cápita VS. Cobertura",
        "Morbilidad per cápita VS. Causa",
        "Familia Causa VS. PIB per cápita ",
        "Familia Causa VS. Edad",
        
    ]

tab3_content = dbc.Card(
    dbc.CardBody(
        [   
            html.H6("Sugerencias:"),
            html.P("A continuación presentamos algunos análisis sugeridos "),
            dcc.RadioItems(
                options=[],
                style={
                    'display':'block'
                }
            )
        ]
    ),
    #className="mt-3",
)
tab4_content = dbc.Card(
    dbc.CardBody(
        [   
            html.H6("Sugerencias:"),
            html.P("A continuación presentamos algunos análisis sugeridos "),
            dcc.RadioItems(
                options=[
                    {'label': row, 'value': row} for row in sugerencias
                ],
                style={
                    'display':'block'
                }
            )
        ]
    ),
    #className="mt-3",
)
tab5_content = dbc.Card(
    dbc.CardBody(
        [   
            html.H6("Sugerencias:"),
            html.P("A continuación presentamos algunos análisis sugeridos "),
            dcc.RadioItems(
                options=[],
                style={
                    'display':'block'
                }
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
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [html.H6("Grupo de datos principal: ")]
                                ),
                                dbc.Col(
                                    [html.H6("Año: ")]
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            id='familia-radio',
                                            options=[{'label': i, 'value': i} for i in ['PQRS SuperSalud', 'Morbilidad', 'Socioeconómico']],
                                            value='PQRS SuperSalud'
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            id='anio-dropdown',
                                            options=[{'label': i, 'value': i} for i in ['2017', '2018', '2019']],
                                            value='2019'
                                        )
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H6("Variable principal: "),
                                        dcc.Dropdown(
                                            id='variable-principal',
                                            options=available_indicators,
                                            value=available_indicators[0]['value']
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        html.H6("Variable secundaria: "),
                                        dcc.Dropdown(
                                            id='variable-secundaria',
                                            options=available_indicators,
                                            value=available_indicators[1]['value']
                                        )
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Graph(id="heatmap-principal"),
                                    ],
                                    md = 12
                                ),
                                html.H1(id="texto")
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [html.H6("Grupo de datos principal: ")]
                                ),
                                dbc.Col(
                                    [html.H6("Año: ")]
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [html.H6("Grupo de datos principal: ")]
                                        ),
                                        dbc.Row(
                                            [html.H6("Año: ")]
                                        ),
                                        dbc.Row(
                                            [dcc.Graph(id="graph-top")]
                                        )
                                    ],
                                    md = 6
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [html.H6("Grupo de datos principal: ")]
                                        ),
                                        dbc.Row(
                                            [html.H6("Año: ")]
                                        ),
                                        dbc.Row(
                                            [dcc.Graph(id="graph-bottom")]
                                        )
                                    ],
                                    md = 6
                                )
                            ]
                        ), 
                    ],
                    md = 8,
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
                        dcc.Graph(id="mapa-principal", clear_on_unhover=True),
                    ],
                    md = 4
                )
            ],
            #style = {
            #    'border-style': 'solid',
            #    'border-width': '1px'
            #}
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
                                            options=available_indicators
                                        )
                                    ]
                                ),
                                
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader("Consultas sugeridas"),
                                        dbc.ModalBody(
                                            dbc.Tabs(
                                                [
                                                    dbc.Tab(tab3_content, label="PRQS SuperSalud"),
                                                    dbc.Tab(tab4_content, label="Morbilidad"),
                                                    dbc.Tab(tab5_content, label="Socioeconómico")
                                                ]
                                            )
                                        ),
                                        dbc.ModalFooter(
                                            dbc.Button(
                                                "Close", id="close-sugerencias", className="ml-auto"
                                            )
                                        ),
                                    ],
                                    id="modal-sugerencias",
                                    centered=True,
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
                                ),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader("Info"),
                                        dbc.ModalBody(
                                            children=
                                            [
                                                html.H3("Integrantes:"),
                                                html.Ul([html.Li(x) for x in integrantes]),
                                                html.H3("Agradecimientos a:"),
                                                html.Img(src = app.get_asset_url("img/logosMinTIC.png"), height="120px"),
                                                html.H3("Fuentes de datos consultadas"),
                                                html.Ul([html.Li(x) for x in fuentesDeDatos]),
                                            ]
                                        ),
                                        dbc.ModalFooter(
                                            dbc.Button(
                                                "Close", id="close-info", className="ml-auto"
                                            )
                                        ),
                                    ],
                                    id="modal-info",
                                    centered=True,
                                )
                            ]
                        ),
                        
                        dash_table.DataTable(
                            id='top10-table',
                            columns=[
                                
                            ],
                            style_table={
                                'maxHeight': '450px',
                                'overflowY': 'scroll',
                                'overflowX': 'scroll'
                            }
                        ),
                        dcc.Graph(
                            figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]},
                            id="grafico-principal"
                        )
                    ],
                    md=8,
                ),
                dbc.Col(
                    [
                        html.H1("MAPA")
                        
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
                html.Img(id="wordcloud-usuario-img", width="300px"),
                html.H1(id="click_txt")
            ]
        )
    ],
    className="mt-4",
)

# #######################################################
#          APP LAYOUT
# #######################################################

app.layout = html.Div([navbar, body])



# #######################################################
#           CALL BACK  - MODAL WINDOWS
# #######################################################

 
@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


 
@app.callback(
    Output("modal-info", "is_open"),
    [Input("open-info", "n_clicks"), Input("close-info", "n_clicks")],
    [State("modal-info", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


 
@app.callback(
    Output("modal-sugerencias", "is_open"),
    [Input("open-sugerencias", "n_clicks"), Input("close-sugerencias", "n_clicks")],
    [State("modal-sugerencias", "is_open")],
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
    municipios = []
    
    if depto != None:
        municipios = municipios_df[municipios_df['COD_DEPTO'] == depto][['MUNICIPIO', 'COD_MUNICIPIO']].values
    
    municipios = [{'label': row[0], 'value': row[1]} for row in municipios]
    return municipios


# #######################################################
#           CALL BACK  - TABLA PRINCIPAL
# #######################################################
def filtrarPQRS(depto, municipio, tipoPersona):
    
    filtroTotal = np.ones((pqrs_df.shape[0], 1), dtype = bool).reshape(-1)
    
    if depto != None:
        filtroTotal = filtroTotal & (pqrs_df['COD_DEPTO'] == depto)

    if municipio != None:
        filtroTotal = filtroTotal & (pqrs_df['COD_MUNICIPIO'] == municipio)
    

    if tipoPersona != '1':
        filtroTotal = filtroTotal & (pqrs_df['AFEC_TIPOPER'] == tipoPersona)


    pqrsFiltrado = pqrs_df[filtroTotal]

    return pqrsFiltrado


@app.callback(
    
        #dash.dependencies.Output(component_id='top10-table', component_property='data'),
        #dash.dependencies.Output(component_id='top10-table', component_property='columns'),
        dash.dependencies.Output("heatmap-principal", "figure")
    ,   
    [
        dash.dependencies.Input(component_id='variable-tabla-dropdown', component_property='value'),
        dash.dependencies.Input(component_id='departamento-dropdown', component_property='value'),
        dash.dependencies.Input(component_id='municipio-dropdown', component_property='value'),
        dash.dependencies.Input(component_id='filtro-cantidades-dropdown', component_property='value'),
        dash.dependencies.Input(component_id='tipo-persona-radiobtn', component_property='value'),
        dash.dependencies.Input(component_id='mejores-peores-radiobtn', component_property='value'),
        dash.dependencies.Input(component_id='variable-principal', component_property='value'),
        dash.dependencies.Input(component_id='variable-secundaria', component_property='value'),
        dash.dependencies.Input(component_id='anio-dropdown', component_property='value'),
        dash.dependencies.Input(component_id='mapa-principal', component_property='hoverData')
    ]
)
def update_top10_table(variableInteres, depto, municipio, cantidades, tipoPersona, mejoresPeores, variablePrincipal, variableSecundaria, anio, hoverData):
    
    pqrsFiltrado = filtrarPQRS(depto, municipio, tipoPersona)

    columnas = [ variableInteres]


    if ((cantidades == None) or ('abs' in cantidades) ):
        columnas += ['2017', '2018', '2019']
    
    if ((cantidades == None) or ('porc' in cantidades) ):
        columnas += ['2017_PORC', '2018_PORC', '2019_PORC']
    
    if ((cantidades == None) or ('variaciones' in cantidades) ):
        columnas += ['2017_2018_PORC', '2018_2019_PORC']
    
    
    if variableInteres == None:
        variableInteres = 'RIESGO_VIDA'
    

    # Tabla
    #dff = consolidadoAnio(variableInteres, pqrsFiltrado)

    if anio == None:
        anio = '2019'
    pqrsFiltrado = pqrsFiltrado[pqrsFiltrado['ANIO'] == anio]
    
    """
    if mejoresPeores == "bottom":
        dff = dff.tail(10)
    else:
        dff = dff.head(10)
    """
    #dff_tabla = dff[columnas]
    #dff_tabla = dff

    ## HEATMAP!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #print(hoverData)
    print("COMPARANDO HEAT " + variablePrincipal + " vs. " +variableSecundaria + " en " +str(anio))
    deptoHover = None
    municipioHover = None
    comparacionNombre = ""
    comparacion = None
    if hoverData != None:
        if 'location' in hoverData['points'][0]:
            deptoHover = hoverData['points'][0]['location']
            print("Comparando depto con " + str(deptoHover))
            comparacionNombre = municipios_df[municipios_df['COD_DEPTO'] == deptoHover]['DEPARTAMENTO'].values[0]

        else:
            municipioHover = hoverData['points'][0]['text']
            municipioHover = int(municipioHover)
            muni_reducido = municipios_df[['MUNICIPIO', 'COD_MUNICIPIO', 'COD_DEPTO', 'DEPARTAMENTO']]
            print("Comparando muni con " + str(municipioHover))
            print(type(municipioHover))
            print(muni_reducido.shape)
            print(muni_reducido[muni_reducido['COD_DEPTO'] == depto])
            print("=> " +muni_reducido[muni_reducido['COD_MUNICIPIO'] == municipioHover])
            print("==> " +muni_reducido[muni_reducido['COD_MUNICIPIO'] == municipioHover]['MUNICIPIO'])
            
            #print("===> " +muni_reducido[muni_reducido['COD_MUNICIPIO'] == municipioHover]['MUNICIPIO'].values)
            #comparacionNombre = municipios_df[municipios_df['COD_MUNICIPIO'] == municipioHover]['MUNICIPIO'].values[0]
            comparacionNombre =" MUNICIOPIO"
            
        pqrsFiltrado = filtrarPQRS(deptoHover, municipioHover, tipoPersona)
        comparacion = [depto, municipio, tipoPersona]
        titulo = "Comparación con " + str( comparacionNombre ) + " => " +variablePrincipal + " vs. " +variableSecundaria + " en " + str(anio)
    else:
        pqrsFiltrado = filtrarPQRS(depto, municipio, tipoPersona)
        titulo = variablePrincipal + " vs. " +variableSecundaria + " en " +anio
    
    f = HeatMap(pqrsFiltrado, variablePrincipal, variableSecundaria, titulo, comparacion)

    return f



def HeatMap(df, var1, var2, titulo="", columnas=None):
    s = pd.crosstab(df[var1],df[var2], margins=True).copy()
    
    

    if columnas == None:
        s = s.sort_values(by="All", ascending=False)
        s = s.sort_values(by="All", ascending=False, axis=1)
        s = s.drop("All")
        s = s.drop("All", axis = 1)
        s = s.iloc[:10, :10]
    else:
        depto = columnas[0]
        municipio = columnas[1]
        tipoPersona = columnas[2]

        original = filtrarPQRS(depto, municipio, tipoPersona)
        crosstabOriginal = pd.crosstab(original[var1],original[var2], margins=True).copy()
        crosstabOriginal = crosstabOriginal.sort_values(by="All", ascending=False)
        crosstabOriginal = crosstabOriginal.sort_values(by="All", ascending=False, axis=1)
        crosstabOriginal = crosstabOriginal.drop("All")
        crosstabOriginal = crosstabOriginal.drop("All", axis = 1)
        crosstabOriginal = crosstabOriginal.iloc[:10, :10]
        print("ORIGINAAAAAAL COLUMNAS")
        #print(crosstabOriginal.columns)
        print(crosstabOriginal.shape)
        print("COMPARACION COLUMNAS")
        #print(s.columns)
        print(s.shape)
        #print("ORIGINAAAAAAL index")
        #print(crosstabOriginal.index)
        #print("COMPARACION index")
        #print(s.index)
        #s = s[crosstabOriginal.index][crosstabOriginal.columns]


        s = s.sort_values(by="All", ascending=False)
        s = s.sort_values(by="All", ascending=False, axis=1)
        s = s.drop("All")
        s = s.drop("All", axis = 1)
        s = s.iloc[:10, :10]




    fig = go.Figure(data=go.Heatmap(
                    z=s,
                    y=s.index,
                    x=s.columns))
    fig.update_layout(
        title=titulo,
        xaxis_title=var1,
        yaxis_title=var2,
    )
    return fig

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
        dash.dependencies.Output("titulo_top_10", "children"),
        dash.dependencies.Output("wordcloud-usuario-img", "src")
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
        nombreDepto = departamentos_df[departamentos_df['COD_DEPTO'] == departamentoSeleccionado][['DEPARTAMENTO']].values[0][0]
        titulo = parte + " 10 - " + nombreDepto
        if municipioSeleccionado != None:
            titulo = parte + " 10 - " + municipioSeleccionado + " (" + nombreDepto + ")"

    paciente = pqrs_df[pqrs_df['AFEC_ID'] == 518513]
    causas = paciente[['MOTIVO_ESPECIFICO', 'PATOLOGIA_1', 'PATOLOGIA_TIPO', 'CIE_10']]
    causas = causas["MOTIVO_ESPECIFICO"].astype(str) +" "+ causas["PATOLOGIA_1"] +" "+ causas["PATOLOGIA_TIPO"] +" "+ causas["CIE_10"]
    causas = causas[~causas.isnull()]
    word_cloud_text = ''.join(causas.tolist())
    wordcloud = WordCloud(max_font_size=100, max_words=100, background_color="white",\
                            scale = 10,width=800, height=400).generate(word_cloud_text)
                            
    fig = plt.figure(figsize = (20, 15))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    #plt.savefig("assets/img/wordcloud_usuario.png")
    urlWC = app.get_asset_url("img/wordcloud_usuario.png")
    
    #dcc.Graph(id=‘graphs’, figure=fig_url)
    return [[html.I(className=icono), titulo], urlWC]


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

    centroide = {"lat": 4, "lon": -72}
    zoom = 3

    if departamentoSeleccionado != None:
        departamentosSeleccionados_df = departamentos_df[departamentos_df['COD_DEPTO'] == departamentoSeleccionado]
        
        lat = (deptos_geo_df[deptos_geo_df['DPTO'] == departamentoSeleccionado]['centroid']).values[0]['coordinates'][1]
        lon = (deptos_geo_df[deptos_geo_df['DPTO'] == departamentoSeleccionado]['centroid']).values[0]['coordinates'][0]
        
        centroide = {"lat": lat, "lon": lon}
        zoom = 6
        
        muncipiosEnDepto_df = m_geo_df[m_geo_df['COD_DEPTO'] == departamentoSeleccionado]
        
        munpoint = go.Scattermapbox(
            lat = muncipiosEnDepto_df['LATITUD'],
            lon = muncipiosEnDepto_df['LONGITUD'],
            mode = 'markers',
            text = muncipiosEnDepto_df['ID_ESPACIA'],
            #marker = dict (size= , color = )
        )     
        capas.append(munpoint)       
        

    g = go.Choroplethmapbox(geojson = geod,
                        locations = departamentosSeleccionados_df['COD_DEPTO'], z = departamentosSeleccionados_df['NUM_PQRS_2019'],
                        colorscale = "Viridis", zmin = 0, zmax = 12,
                        marker_opacity = 0.5, marker_line_width = 0, hovertext = departamentosSeleccionados_df['DEPARTAMENTO'])
    capas.append(g)

    if departamentoSeleccionado != None:
        capas.append(munpoint)


    lyt = go.Layout(mapbox_style = "carto-positron",
                mapbox_zoom = zoom, mapbox_center = centroide)
    
    
    
    fig = go.Figure(data = capas,layout = lyt)
    return fig


@app.callback(
    dash.dependencies.Output(component_id='click_txt', component_property='children'),
    [dash.dependencies.Input(component_id='linkSugeridos', component_property='n_clicks')]
)
def clickEnLink(varC):
    print(varC)
    return "click click"


if __name__ == "__main__":
    app.run_server(debug=True)