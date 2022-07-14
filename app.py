import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import json
import numpy as np
from urllib.request import urlopen
import gc


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

# -- Import and clean data (importing csv into pandas)

df_tipo_delito = pd.read_csv(r'datos\tipo_delito.csv',encoding='latin-1',index_col=0)
df_ST = pd.read_csv(r'datos\Incidencia_Delictiva_Full_Series_Tiempo.csv',encoding='latin-1',index_col=0)
df_estados = pd.read_csv(r'datos\estados.csv',encoding='latin-1',index_col=0)

df_estados_bar = df_estados
nueva_fila = {'estado':'Todos'}
#añadiendo la nueva fila al dataFrame
df_estados_bar = df_estados_bar.append(nueva_fila, ignore_index=True)

def getDFYear(_year):
    gc.collect()
    df = pd.read_csv(rf'datos\Incidencia_Delictiva_Full_ids-Name_{_year}.csv',encoding='latin-1')
    return df

def getDFTipoDelito(_df,_tipo_delito):
    return _df[ _df['tipo_delito']==_tipo_delito ]

def getDFCantidad(_df,_year):
    _df["fecha"]= pd.to_datetime(_df["fecha"])

    df_cantidad_tot = (_df.groupby([_df['fecha'].map(lambda x: x.year),'id_name'])['cantidad'].sum())
    df_cantidad_tot = pd.DataFrame(df_cantidad_tot[(_year)])
    df_cantidad_tot = df_cantidad_tot.reset_index()
    return df_cantidad_tot

def getDFEstadoTipoDelito():
    gc.collect()
    _df = pd.read_csv(rf'datos\Incidencia_Delictiva_Full_Estado_TipoDelito.csv',encoding='latin-1')
    return _df

def getDFMunicipioTipoDelito(_year):
    gc.collect()
    _df = pd.read_csv(rf'datos\Incidencia_Delictiva_Full_Estado_Municipio_TipoDelito_{_year}.csv',encoding='latin-1',index_col=0)
    return _df

geojson = 'https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json'
with urlopen(geojson) as response:
  estados = json.load(response)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

        html.H1("Incidencia delictiva en México", style={'text-align': 'center'}),

        dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
            dcc.Tab(label='Series de tiempo', value='tab-1', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Mapa', value='tab-2', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Mapa de árbol Estatal', value='tab-3', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Mapa de árbol Municipal', value='tab-4', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Graficas de barras', value='tab-5', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Graficas de barras Municipios', value='tab-6', style=tab_style, selected_style=tab_selected_style),
        ], style=tabs_styles),

        html.Div(id='tabs-content-inline'),

])

@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Br(),
            html.Div([

                html.Div([
                    dcc.Dropdown(df_tipo_delito['tipo_delito'],
                                id='tipo-delito',
                                value='Homicidio')
                ], style={'width': '98%', 'float': 'right', 'display': 'inline-block'}),
            ]),
            html.Br(),

            html.Div([
                dcc.Graph(id='series_time', figure={})
            ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),

        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Br(),

            html.Div([
                html.Div([
                    dcc.Dropdown(id="anio",
                                    options=[
                                        {"label": "2015", "value": 2015},
                                        {"label": "2016", "value": 2016},
                                        {"label": "2017", "value": 2017},
                                        {"label": "2018", "value": 2018},
                                        {"label": "2019", "value": 2019},
                                        {"label": "2020", "value": 2020},
                                        {"label": "2021", "value": 2021},
                                        {"label": "2022", "value": 2022}],
                                    multi=False,
                                    value=2015,
                        )
                ], style={'width': '48%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Dropdown(df_tipo_delito['tipo_delito'],
                                id='tipo-delito',
                                value='Homicidio')
                ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
            ]),

            html.Div([
                dcc.Graph(id='my_bee_map', figure={})
            ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
            
        ])
    elif tab == 'tab-3':
        return html.Div([
            
            html.Br(),
            html.Div([
                html.Div([
                    dcc.Dropdown(id="anio",
                                    options=[
                                        {"label": "Todos", "value": 'Todos'},
                                        {"label": "2015", "value": 2015},
                                        {"label": "2016", "value": 2016},
                                        {"label": "2017", "value": 2017},
                                        {"label": "2018", "value": 2018},
                                        {"label": "2019", "value": 2019},
                                        {"label": "2020", "value": 2020},
                                        {"label": "2021", "value": 2021},
                                        {"label": "2022", "value": 2022}],
                                    multi=False,
                                    value='Todos',
                        )
                    ], style={'width': '48%', 'display': 'inline-block'}),
            ]),


            html.Div([
                dcc.Graph(id='tree_map', figure={})
            ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),

            
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.Br(),
            html.Div([

                html.Div([
                    dcc.Dropdown(id="anio_map",
                                    options=[
                                        {"label": "2015", "value": 2015},
                                        {"label": "2016", "value": 2016},
                                        {"label": "2017", "value": 2017},
                                        {"label": "2018", "value": 2018},
                                        {"label": "2019", "value": 2019},
                                        {"label": "2020", "value": 2020},
                                        {"label": "2021", "value": 2021},
                                        {"label": "2022", "value": 2022}],
                                    multi=False,
                                    value=2015,
                        )
                ], style={'width': '48%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Dropdown(df_estados['estado'],
                                id='estados',
                                value='Guanajuato')
                ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
            ]),
            html.Br(),
            html.Div([
                dcc.Graph(id='tree_municipal_map', figure={})
            ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
        ])
    elif tab == 'tab-5':
        return html.Div([
            html.Br(),
            html.Div([
                html.Div([
                    dcc.Dropdown(df_tipo_delito['tipo_delito'],
                                id='tipo-delito_bar',
                                value='Homicidio')
                ], style={'width': '98%', 'float': 'right', 'display': 'inline-block'}),
            ]),
            html.Br(),
            html.Div([
                dcc.Graph(id='delitos_bar', figure={})
            ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
        ])
    elif tab == 'tab-6':
        return html.Div([
            html.Br(),
            html.Div([
                
                html.Div([
                    dcc.Dropdown(id="anio_bar_mun",
                                    options=[
                                        {"label": "2015", "value": 2015},
                                        {"label": "2016", "value": 2016},
                                        {"label": "2017", "value": 2017},
                                        {"label": "2018", "value": 2018},
                                        {"label": "2019", "value": 2019},
                                        {"label": "2020", "value": 2020},
                                        {"label": "2021", "value": 2021},
                                        {"label": "2022", "value": 2022}],
                                    multi=False,
                                    value=2015,
                        )
                ], style={'width': '30%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Dropdown(df_tipo_delito['tipo_delito'],
                                id='tipo-delito_bar_mun',
                                value='Homicidio')
                ], style={'width': '30%', 'float': 'right', 'display': 'inline-block'}),

                html.Div([
                    dcc.Dropdown(df_estados_bar['estado'],
                                id='estados_bar_mun',
                                value='Todos')
                ], style={'width': '30%', 'display': 'inline-block', 'padding': '0 20'}),
            ]),
            html.Br(),
            html.Div([
                dcc.Graph(id='delitos_bar_mun', figure={})
            ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
        ])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

@app.callback(
    Output(component_id='series_time', component_property='figure'),
    Input(component_id='tipo-delito', component_property='value')
)
def create_time_series(tipo_delito):
    df_tp_s = df_ST
    df_tp_s = df_tp_s[ df_tp_s['tipo_delito']== tipo_delito ]
    df_series = df_tp_s.drop(['tipo_delito'], axis=1)
    df_series = df_series.drop(['sub_tipo_delito'], axis=1)
    df_series = df_series.groupby(['fecha']).sum()
    df_series = df_series.reset_index()

    fig = px.line(df_series, x="fecha", y=df_series.columns,
                hover_data={"fecha": "|%B %d, %Y"},
                title= f'Casos de {tipo_delito} en Mexico 2015-2022')
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        ticklabelmode="period")
        
    return fig

@app.callback(
    Output(component_id='my_bee_map', component_property='figure'),
    Input(component_id='anio', component_property='value'),
    Input(component_id='tipo-delito', component_property='value')
)
def update_graph(anio,tipo_delito):
    df = getDFYear(anio)
    df = getDFTipoDelito(df,tipo_delito)
    df = getDFCantidad(df,anio)

    max_cantidad = df['cantidad'].max()

    # Plotly Express
    fig = px.choropleth_mapbox(
        df,
        geojson=estados,
        locations='id_name',
        mapbox_style="carto-positron",
        zoom=3.8,
        color="cantidad",
        center= {"lat": 25.67507, "lon": -100.31847},
        color_continuous_scale=["green", "orange","red"],
        range_color=(0, max_cantidad),
        labels={"cantidad": "cantidad"},
        opacity=0.5,
        height= 600
    )

    fig.update_layout(
        title_text= f"Casos de {tipo_delito} en México {anio}",
        title_xanchor="center",
        title_font=dict(size=24),
        title_x=0.5,
        geo=dict(scope='usa'),
    )

    return fig

@app.callback(
    Output(component_id='tree_map', component_property='figure'),
    Input(component_id='anio', component_property='value'),
)
def tree_graph(anio):
    _df = getDFEstadoTipoDelito()
    print(anio)
    if anio != 'Todos':
        _df = _df[_df["fecha"].between(f'{anio}-01-01', '{anio}-12-31')]
    else: 
        anio = '2015 -2022'
    fig = px.treemap(
        _df, 
        path=['estado', 'tipo_delito'], 
        values='cantidad',
        title= f"Casos de delitos en México {anio}",
        height= 570
    )

    fig.update_layout(
        title_xanchor="center",
        margin = dict(t=50, l=25, r=25, b=25)
    )

    return fig

@app.callback(
    Output(component_id='tree_municipal_map', component_property='figure'),
    Input(component_id='anio_map', component_property='value'),
    Input(component_id='estados', component_property='value'),
)
def tree_municipal_graph(_year,estado):
    _df = getDFMunicipioTipoDelito(_year)
    df_mun = _df[_df['estado']==estado]
    print(df_mun)
    

    fig = px.treemap(
        df_mun, 
        path=['municipio', 'tipo_delito'], 
        values='cantidad',
        title= f"Casos de delitos en {estado}",
        height= 570
    )

    fig.update_layout(
        title_xanchor="center",
        margin = dict(t=50, l=25, r=25, b=25)
    )

    return fig

@app.callback(
    Output(component_id='delitos_bar', component_property='figure'),
    Input(component_id='tipo-delito_bar', component_property='value'),
)
def bar_delitos_graph(tipo_delito):
    _df = getDFEstadoTipoDelito()
    df_bar = _df[_df['tipo_delito']==tipo_delito]
    df_bar = df_bar.groupby(['tipo_delito','estado'])['cantidad'].sum()
    df_bar = df_bar.reset_index()
    df_bar = df_bar.sort_values(by=['cantidad'])
    cantidad_max = df_bar['cantidad'].max()

    fig = px.bar(df_bar, x='estado', y='cantidad',
            color="cantidad",
            color_continuous_scale=["green", "orange","red"],
            range_color=(0, cantidad_max),
             labels={'pop':'population of Canada'}, height=400)
    

    return fig

@app.callback(
    Output(component_id='delitos_bar_mun', component_property='figure'),
    Input(component_id='anio_bar_mun', component_property='value'),
    Input(component_id='estados_bar_mun', component_property='value'),
    Input(component_id='tipo-delito_bar_mun', component_property='value'),
)
def bar_delitos__mun_graph(_year,estado,tipo_delito):
    _df = getDFMunicipioTipoDelito(_year)
    df_bar = _df[_df['tipo_delito']==tipo_delito]
    if(estado != 'Todos'):
        df_bar = _df[_df['estado']==estado]
    df_bar = df_bar.drop(['estado'], axis=1)
    df_bar = df_bar.drop(['sub_tipo_delito'], axis=1)
    df_bar = df_bar.drop(['id_name'], axis=1)
    df_bar = df_bar[df_bar['tipo_delito']==tipo_delito]
    print(df_bar)
    df_bar = df_bar.groupby(['municipio'])['cantidad'].sum()
    df_bar = df_bar.reset_index()
    df_bar = df_bar.sort_values(by=['cantidad'],ascending=False)
    cantidad_max = df_bar['cantidad'].max()

    if(estado == 'Todos'):
        df_bar = df_bar.head(20)

    fig = px.bar(df_bar, x='cantidad', y='municipio',
            orientation='h',
            color="cantidad",
            color_continuous_scale=["orange","red"],
            range_color=(0, cantidad_max),
             labels={'pop':'Casos en México'}, height=700)
    

    return fig



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)