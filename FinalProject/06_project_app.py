import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table

df = pd.read_csv('aggr.csv', parse_dates=['Entry time'])

df['YearMonth'] = pd.to_datetime(df['Entry time'].map(lambda x: x.strftime('%Y')))

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
                                    dcc.DatePickerRange(
                                        id="date-range-filter",
                                        display_format="MMM YY",
                                        start_date=df['Entry time'].min(),
                                        end_date=df['Entry time'].max()
                                    ),
                                    html.H6("Departamento:"),
                                    dcc.Dropdown(
                                        id='departamento-dropdown',
                                        options=[
                                            {'label': 'Amazonas', 'value': 'NYC'},
                                            {'label': 'Antioquia', 'value': 'MTL'},
                                            {'label': 'Atlántico', 'value': 'SF'}
                                        ],
                                    ),
                                    html.H6("Municipio:"),
                                    dcc.Dropdown(
                                        id='municipio-dropdown',
                                        options=[
                                            {'label': 'El Encanto', 'value': 'NYC'},
                                            {'label': 'Leticia', 'value': 'MTL'},
                                            {'label': 'Puerto Nariño', 'value': 'SF'}
                                        ],
                                    ),
                                    html.H6("Institución:"),
                                    dcc.Dropdown(
                                        id='institucion-dropdown',
                                        options=[
                                            {'label': 'El Encanto', 'value': 'NYC'},
                                            {'label': 'Leticia', 'value': 'MTL'},
                                            {'label': 'Puerto Nariño', 'value': 'SF'}
                                        ],
                                    )
                                ]
                            )
                        ]
                    ),
                    html.P('Strategy Returns', className="six columns"),
                    html.Div(
                        className="three columns",
                        children=[
                            html.H3("Top 10"),
                    dash_table.DataTable(
                        id='top10',
                        columns=[
                            {'name': 'Municipio', 'id': 'Number'},
                            {'name': 'Total', 'id': 'Trade type'}
                        ],
                        #style_cell={'width': '50px'},
                        style_table={
                            'maxHeight': '450px',
                            'overflowY': 'scroll'
                        }
                    )]
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




if __name__ == "__main__":
    app.run_server(debug=True)