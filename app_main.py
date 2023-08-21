import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine


db_connection = mysql.connector.connect() #credenciais do MySQL
connection = mysql.connector.connect(**db_config)

bases_individuais = pd.read_excel('base_atualizada_2.xlsx')

def criar_tabela(data, sugestao):
    df = pd.DataFrame({'Sugestão {}'.format(sugestao): data})
    table = dbc.Table.from_dataframe(df, striped=True, bordered=False, borderless = True, hover=True,color = 'primary',size = 'sm')
    return table


def otimizar_letras(letras_input,duplas_2,bases_individuais):
    primeiro_df = 0
    df1 = letras_input
    base_2 = duplas_2
    common_columns = df1.columns.intersection(base_2.columns)
    base_1 = bases_individuais[bases_individuais[common_columns].le(df1.iloc[0][common_columns]).all(axis=1)]
    filtered_df2 = base_2

    if len(base_2)==0:
        return(base_1)
    if len(filtered_df2) <50:
        amostra = len(filtered_df2)
    else:
        amostra = 50
    filtered_df2 = filtered_df2.sample(n=amostra).reset_index(drop = True)
    filtered_base = bases_individuais[bases_individuais[common_columns].le(df1.iloc[0][common_columns]).all(axis=1)]
    for i in range(amostra):
        id_1 = filtered_df2.loc[i]['ID_1']
        id_2 = filtered_df2.loc[i]['ID_2']
        id_1_verdadeiro = filtered_df2.loc[i]['ID_1_verdadeiro']
        id_2_verdadeiro = filtered_df2.loc[i]['ID_2_verdadeiro']
        linha = filtered_df2.iloc[[i]]
        if len(filtered_base) <50:
            amostra = len(filtered_base)
        else:
            amostra = 50
        filtered_base_intermed = filtered_base.sample(n=amostra).reset_index(drop = True)
        for j in common_columns:
            filtered_base_intermed[j] += filtered_df2.loc[i][j]
        filtered_base_intermed = filtered_base_intermed.drop(columns=['value','Tipo','minusculas', 'prioridade','album']).rename(columns={'ID': 'ID_3_verdadeiro', 'ID_combinacao': 'ID_3'})
        filtered_base_intermed = filtered_base_intermed[filtered_base_intermed[common_columns].le(df1.iloc[0][common_columns]).all(axis=1)]
        filtered_base_intermed['ID_1'] = id_1
        filtered_base_intermed['ID_2'] = id_2
        filtered_base_intermed['ID_1_verdadeiro'] = id_1_verdadeiro
        filtered_base_intermed['ID_2_verdadeiro'] = id_2_verdadeiro
        filtered_base_intermed = filtered_base_intermed[filtered_base_intermed['ID_3_verdadeiro'] != filtered_base_intermed['ID_2_verdadeiro']]
        filtered_base_intermed = filtered_base_intermed[filtered_base_intermed['ID_3_verdadeiro'] != filtered_base_intermed['ID_1_verdadeiro']]

        try:
            primeiro_df = pd.concat([primeiro_df, filtered_base_intermed], ignore_index=True)
        except:
            primeiro_df = filtered_base_intermed

    base_3 = primeiro_df
    if len(base_3) == 0:
        return(base_2)
    #parte 4
    filtered_df2 = primeiro_df
    primeiro_df = 0
    if len(filtered_df2) <50:
        amostra = len(filtered_df2)
    else:
        amostra = 50
    filtered_df2 = filtered_df2.sample(n=amostra).reset_index(drop = True)
    filtered_base = bases_individuais[bases_individuais[common_columns].le(df1.iloc[0][common_columns]).all(axis=1)]
    for i in range(amostra):
        id_1 = filtered_df2.loc[i]['ID_1']
        id_2 = filtered_df2.loc[i]['ID_2']
        id_1_verdadeiro = filtered_df2.loc[i]['ID_1_verdadeiro']
        id_2_verdadeiro = filtered_df2.loc[i]['ID_2_verdadeiro']
        id_3 = filtered_df2.loc[i]['ID_3']
        id_3_verdadeiro = filtered_df2.loc[i]['ID_3_verdadeiro']

        linha = filtered_df2.iloc[[i]]
        if len(filtered_base) <50:
            amostra = len(filtered_base)
        else:
            amostra = 50
        filtered_base_intermed = filtered_base.sample(n=amostra).reset_index(drop = True)
        for j in common_columns:
            filtered_base_intermed[j] += filtered_df2.loc[i][j]
        filtered_base_intermed = filtered_base_intermed.drop(columns=['value','Tipo','minusculas', 'prioridade','album']).rename(columns={'ID': 'ID_4_verdadeiro', 'ID_combinacao': 'ID_4'})
        filtered_base_intermed = filtered_base_intermed[filtered_base_intermed[common_columns].le(df1.iloc[0][common_columns]).all(axis=1)]
        filtered_base_intermed['ID_1'] = id_1
        filtered_base_intermed['ID_2'] = id_2
        filtered_base_intermed['ID_1_verdadeiro'] = id_1_verdadeiro
        filtered_base_intermed['ID_2_verdadeiro'] = id_2_verdadeiro
        filtered_base_intermed['ID_3'] = id_3
        filtered_base_intermed['ID_3_verdadeiro'] = id_3_verdadeiro
        filtered_base_intermed = filtered_base_intermed[filtered_base_intermed['ID_4_verdadeiro'] != filtered_base_intermed['ID_2_verdadeiro']]
        filtered_base_intermed = filtered_base_intermed[filtered_base_intermed['ID_4_verdadeiro'] != filtered_base_intermed['ID_1_verdadeiro']]
        filtered_base_intermed = filtered_base_intermed[filtered_base_intermed['ID_4_verdadeiro'] != filtered_base_intermed['ID_3_verdadeiro']]

        try:
            primeiro_df = pd.concat([primeiro_df, filtered_base_intermed], ignore_index=True)
        except:
            primeiro_df = filtered_base_intermed
    #5
    base_4 = primeiro_df
    if len(base_4) ==0:
        return(base_3)

    filtered_df2 = primeiro_df
    primeiro_df = 0
    if len(filtered_df2) <50:
        amostra = len(filtered_df2)
    else:
        amostra = 50
    filtered_df2 = filtered_df2.sample(n=amostra).reset_index(drop = True)
    filtered_base = bases_individuais[bases_individuais[common_columns].le(df1.iloc[0][common_columns]).all(axis=1)]
    for i in range(amostra):
        id_1 = filtered_df2.loc[i]['ID_1']
        id_2 = filtered_df2.loc[i]['ID_2']
        id_1_verdadeiro = filtered_df2.loc[i]['ID_1_verdadeiro']
        id_2_verdadeiro = filtered_df2.loc[i]['ID_2_verdadeiro']
        id_3 = filtered_df2.loc[i]['ID_3']
        id_3_verdadeiro = filtered_df2.loc[i]['ID_3_verdadeiro']
        id_4 = filtered_df2.loc[i]['ID_4']
        id_4_verdadeiro = filtered_df2.loc[i]['ID_4_verdadeiro']


        linha = filtered_df2.iloc[[i]]
        if len(filtered_base) <50:
            amostra = len(filtered_base)
        else:
            amostra = 50
        filtered_base_intermed = filtered_base.sample(n=amostra).reset_index(drop = True)
        for j in common_columns:
            filtered_base_intermed[j] += filtered_df2.loc[i][j]
        filtered_base_intermed = filtered_base_intermed.drop(columns=['value','Tipo','minusculas', 'prioridade','album']).rename(columns={'ID': 'ID_5_verdadeiro', 'ID_combinacao': 'ID_5'})
        filtered_base_intermed = filtered_base_intermed[filtered_base_intermed[common_columns].le(df1.iloc[0][common_columns]).all(axis=1)]

        filtered_base_intermed['ID_1'] = id_1
        filtered_base_intermed['ID_2'] = id_2
        filtered_base_intermed['ID_1_verdadeiro'] = id_1_verdadeiro
        filtered_base_intermed['ID_2_verdadeiro'] = id_2_verdadeiro
        filtered_base_intermed['ID_3'] = id_3
        filtered_base_intermed['ID_3_verdadeiro'] = id_3_verdadeiro
        filtered_base_intermed['ID_4'] = id_4
        filtered_base_intermed['ID_4_verdadeiro'] = id_4_verdadeiro

        filtered_base_intermed = filtered_base_intermed[filtered_base_intermed['ID_5_verdadeiro'] != filtered_base_intermed['ID_2_verdadeiro']]
        filtered_base_intermed = filtered_base_intermed[filtered_base_intermed['ID_5_verdadeiro'] != filtered_base_intermed['ID_1_verdadeiro']]
        filtered_base_intermed = filtered_base_intermed[filtered_base_intermed['ID_5_verdadeiro'] != filtered_base_intermed['ID_3_verdadeiro']]
        filtered_base_intermed = filtered_base_intermed[filtered_base_intermed['ID_5_verdadeiro'] != filtered_base_intermed['ID_4_verdadeiro']]

        try:
            primeiro_df = pd.concat([primeiro_df, filtered_base_intermed], ignore_index=True)
        except:
            primeiro_df = filtered_base_intermed
    base_5 = primeiro_df
    if len(base_5) == 0:
        return(base_4)
    return (base_5)


app = dash.Dash(__name__,
external_stylesheets=[dbc.themes.DARKLY,'https://drive.google.com/uc?export=download&id=1M1XOtesUvdBHVoEkM9HGXt9Z83c2iXxi'], #'https://drive.google.com/uc?export=download&id=1M1XOtesUvdBHVoEkM9HGXt9Z83c2iXxi',
title = 'Make the Friendship Bracelets!')
select_letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ124'

app.layout = html.Div(
    children=[
    html.Meta(
        name='viewport',
        content='width=device-width, initial-scale=1.0'
        ),
    html.H1(
        children='Make the Friendship Bracelets!',
        style={
            'textAlign': 'center',
            'color':'white'
        }
    ),
    html.Div(
        children="Receba sugestões para seus Friendship Bracelets baseado nas letras que você possui.",
        style={
            'textAlign': 'center',
            'color': 'white'
        }
    ),
    html.Div(
        children="Selecione abaixo a opção desejada:",
        style={
            'textAlign': 'center',
            'color': 'white'
        }
    ),
    dbc.Row(
        dbc.Col(
            html.Div(
                children=[
                    dbc.RadioItems(
                        id="radios",
                        className="btn-group",
                        inputClassName="btn-check btn-danger",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Buscar Títulos", "value": 'titulos'},
                            {"label": "Buscar Trechos", "value": 'trechos'},
                            {"label": "Otimizar Bracelets!", "value": 'otimizar'},
                        ],
                        value='titulos'
                    ),
                ],
                className="radio-group",
                style={
                    "display": "flex",
                    "justify-content": "center",
                }
            )
        ),
        className="m-0"
    ),
    html.Div(
        id='conditional-panel-titulos'
    ),
    html.Div(
        id='div-tenho-nao',
        children=[
            dbc.RadioItems(
                options=[
                    {"label": "Letras que não tenho", "value": 'nao_tenho'},
                    {"label": "Letras que tenho", "value": 'tenho'},
                ],
                value = 'tenho',
                id="tenho_ou_nao",
                inline=True,
            )
        ],
        style={
            "justify-content": "center",
            "align-items": "center",
            'display': 'none'
        }
    ),
    html.Div(
        id ='div-dropdowns',
        children = [
            "Selecione a quantidade de cada letra que você possui",
            dbc.Row(
                [dbc.Col(
                    [dbc.Label(
                        f'{i}:',
                        html_for=f'dropdown-{i}'
                    ),
                    dbc.Select(
                        id=f'dropdown-{i}',
                        options=['0','1','2','3','4','5'],
                        value='0',
                        size='sm',
                        style={
                            'width': '100%',
                            "justify-content": "center"
                        },
                    ),
                    ],
                    width='auto',
                )
                for i in select_letras[0:7]
                ],
                className="g-0",
                style={
                    "justify-content": "center",
                    'width':'100%',
                    "align-items": 'center'
                }
            ),
            dbc.Row(
                [dbc.Col(
                    [dbc.Label(
                        f'{i}:',
                        html_for=f'dropdown-{i}'
                    ),
                    dbc.Select(
                        id=f'dropdown-{i}',
                        options=['0','1','2','3','4','5'],
                        value='0',
                        size='sm',
                        style={
                            'width': '100%',
                            "justify-content": "center"
                        },
                    ),
                    ],
                    width='auto',
                )
                for i in select_letras[7:14]
                ],
                className="g-0",
                style={
                    "justify-content": "center",
                    'width':'100%',
                    "align-items": 'center'
                }
            ),
            dbc.Row(
                [dbc.Col(
                    [dbc.Label(
                        f'{i}:',
                        html_for=f'dropdown-{i}'
                    ),
                    dbc.Select(
                        id=f'dropdown-{i}',
                        options=['0','1','2','3','4','5'],
                        value='0',
                        size='sm',
                        style={
                            'width': '100%',
                            "justify-content": "center"
                        },
                    ),
                    ],
                    width='auto',
                )
                for i in select_letras[14:21]
                ],
                className="g-0",
                style={
                    "justify-content": "center",
                    'width':'100%',
                    "align-items": 'center'
                }
            ),
            dbc.Row(
                [dbc.Col(
                    [dbc.Label(
                        f'{i}:',
                        html_for=f'dropdown-{i}'
                    ),
                    dbc.Select(
                        id=f'dropdown-{i}',
                        options=['0','1','2','3','4','5'],
                        value='0',
                        size='sm',
                        style={
                            'width': '100%',
                            "justify-content": "center"
                        },
                    ),
                    ],
                    width='auto',
                )
                for i in select_letras[21:28]
                ],
                className="g-0",
                style={
                    "justify-content": "center",
                    'width':'100%',
                    "align-items": 'center'
                }
            ),
            dbc.Row(
                [dbc.Col(
                    [dbc.Label(
                        f'{i}:',
                        html_for=f'dropdown-{i}'
                    ),
                    dbc.Select(
                        id=f'dropdown-{i}',
                        options=['0','1','2','3','4','5'],
                        value='0',
                        size='sm',
                        style={
                            'width': '100%',
                            "justify-content": "center"
                        },
                    ),
                    ],
                    width='auto',
                )
                for i in select_letras[28:29]
                ],
                className="g-0",
                style={
                    "justify-content": "center",
                    'width':'100%',
                    "align-items": 'center'
                }
            )
        ],
            style={'display': 'none'}
    ),
    html.Div(
        id='conditional-panel-botoes'
    )
    ],
    style={
        "justify-content": "center",
        'width':'100%',
        "align-items": 'center'
    }
    )


@app.callback(
    Output('conditional-panel-titulos', 'children'),
    [Input('radios', 'value')]
)
def update_conditional_panel_titulos(selected_value):
    if selected_value == 'titulos':
        return html.Div(
            [html.H3(
                'Buscar Títulos',
                style={
                    'textAlign': 'center',
                    'color': 'white'
                }
            ),
            html.Div(
            children=[
            html.Div(
                "Procurar os títulos utilizando:"
            )
            ],
            style={
                'textAlign': 'center',
                'color': 'white'
            }
            ),
            ]
        )
    elif selected_value == 'trechos':
        return html.Div(
            [html.H3(
                'Buscar Trechos',
                style={
                    'textAlign': 'center',
                    'color': 'white'
                }
            ),
            ],
            style={
                "justify-content": "center",
                'width':'100%',
                "align-items": 'center',
                'textAlign': 'center'
            },
            )
    else:
        return html.Div(
            [html.H3(
                'Otimizar Bracelets!',
                style={
                    'textAlign': 'center',
                    'color': 'white'
                }
            ),
            "A função tenta encontrar o número máximo de bracelets que você consegue formar",
            ],
            style={
                "justify-content": "center",
                'width':'100%',
                "align-items": 'center',
                'textAlign': 'center'
            },
            )


@app.callback(
    Output('conditional-panel-botoes', 'children'),
    [Input('radios', 'value')],
    [Input('tenho_ou_nao', 'value')]

)
def update_conditional_panel_botoes(selected_value, selected_value_tenho):
    if selected_value == 'titulos':
        if selected_value_tenho == 'nao_tenho':
            return html.Div(
                [html.Div(
                    ["Digite as letras que você não possui:",
                    ]
                ),
                dbc.Row(
                    [dbc.Col(
                        [dbc.InputGroup(
                            [dbc.Input(
                                id="input-group-button-letras",
                                placeholder="name"
                            ),
                            dbc.Select(
                                id='dropdown-album',
                                options=[
                                    'Todos','Debut', 'Fearless',
                                    'Speak Now', 'Red', '1989',
                                    'Reputation', 'Lover','folklore',
                                    'evermore', 'Midnights'
                                    ],
                                    value='Todos',
                                    size='sm',
                            ),
                            dbc.Button(
                                "Pesquisar",
                                id="input-group-pesquisar-nao-tenho",
                                n_clicks=0
                            ),
                            ]
                        )
                        ],
                        width='auto',
                    )
                    ],
                    className="g-0",
                    style={
                        "justify-content": "center",
                        'width':'100%',
                        "align-items": 'center'
                    }
                ),
                dbc.Row(
                    [dbc.Col(
                        html.Div(
                            id='tabela-primeira-func'
                        ),
                        xs = 10, sm =10 , md = 10,
                        lg = 4, xl = 4
                    )
                    ],
                    className = 'g-0',
                    style={
                        "justify-content": "center",
                        'width':'100%',
                        "align-items": 'center',
                        'margin-top':'5px'
                    }
                ),
                ],
                style={
                    'textAlign': 'center',
                    'margin': '0 auto',
                    'margin-top':'2px'
                }
            )
        else:
            return html.Div(
                [html.Div(
                    [dbc.Row(
                        [dbc.Col(
                            [dbc.InputGroup(
                                [dbc.Select(
                                    id='dropdown-album-tenho',
                                    options=['Todos','Debut', 'Fearless',
                                    'Speak Now', 'Red', '1989',
                                    'Reputation', 'Lover','folklore',
                                    'evermore', 'Midnights'
                                    ],
                                    value='Todos',
                                    size='md',
                                ),
                                dbc.Button(
                                    "Pesquisar",
                                    id="input-group-pesquisar-tenho",
                                    n_clicks=0
                                )
                                ],
                                style = {
                                    'margin-top':'5px'
                                }
                            )
                            ],
                            width='auto',
                        )
                        ],
                        className="g-0",
                        style={
                            "justify-content": "center",
                            'width':'100%',
                            "align-items": 'center'
                        }
                    )
                    ],
                    style={
                        "justify-content": "center",
                        'width':'100%',
                        "align-items": 'center',
                        'textAlign': 'center'
                    }
                ),
                dbc.Row(
                    [dbc.Col(
                        html.Div(id='tabela-segunda-func'),
                        xs = 10, sm =10 , md = 10,
                        lg = 4, xl = 4
                    )
                    ],
                    className = 'g-0',
                    style={
                        "justify-content": "center",
                        'width':'100%',
                        "align-items": 'center',
                        'margin-top':'5px'
                    }
                ),
                ],
                style={
                    "justify-content": "center",
                    'width':'100%',
                    "align-items": 'center',
                    'textAlign': 'center'
                },
            )

    elif selected_value == 'trechos':
        return html.Div(
            [dbc.Row(
                [dbc.Col(
                    [dbc.InputGroup(
                        [dbc.Select(
                        id=f'dropdown-album-terceira',
                        options=[
                            'Debut', 'Fearless', 'Speak Now',
                            'Red', '1989', 'Reputation',
                            'Lover','folklore', 'evermore', 'Midnights'
                        ],
                        value='Debut',
                        size='sm',
                        ),
                        dbc.Select(
                            id=f'dropdown-musica-terceira',
                            size='sm',
                        )
                        ]
                    )
                    ],
                    width ='auto'
                )
                ],
                className="g-0",
                style={
                    "justify-content": "center",
                    'width':'100%',
                    "align-items": 'center'
                }
            ),
            dbc.Button(
                "Pesquisar",
                id="input-group-pesquisar_trechos",
                n_clicks=0,
                style = {'margin-top':'5px'}
            ),
            html.Div(id='tabela-terceira-func'
        )
        ],
        style={
            "justify-content": "center",
            'width':'100%',
            "align-items": 'center',
            'textAlign': 'center'
        },
    )

    else:
        return html.Div([
            dbc.Button("Pesquisar", id="input-group-pesquisar_otimizar", n_clicks=0,
            style = {'margin-top':'5px'}),
            dbc.Row([dbc.Col(html.Div(id='tabela-quarta-func'),
                xs = 10, sm =10 , md = 10, lg = 4, xl = 4
                )],className = 'g-0', style={"justify-content": "center", 'width':'100%',"align-items": 'center','margin-top':'5px'}),
], style={"justify-content": "center", 'width':'100%',"align-items": 'center', 'textAlign': 'center'},
)

@app.callback(
    Output('tabela-primeira-func', 'children'),
    [Input('input-group-pesquisar-nao-tenho', 'n_clicks')],
    [Input('input-group-button-letras', 'value')],
    [Input('dropdown-album', 'value')]
)
def update_tabela_primeira_func(botao, letras_n_tenho, album_atual):
    if botao == 0:
        return dash.no_update
    if album_atual == 'Todos':
        bases_individuais_atual = bases_individuais
    else:
        bases_individuais_atual = bases_individuais[bases_individuais['album']==album_atual]
    for i in letras_n_tenho:
        if i.lower() in 'abcdefghijklmnopqrstuvwxyz124':
            bases_individuais_atual = bases_individuais_atual[bases_individuais_atual[i.lower()] == 0]
    bases_individuais_atual['Músicas'] = bases_individuais_atual['value']
    bases_individuais_atual = bases_individuais_atual.sort_values('prioridade').reset_index(drop = True).drop_duplicates(subset = 'ID').reset_index(drop = True)
    bases_individuais_atual = bases_individuais_atual.sort_values('ID').reset_index(drop = True)
    bases_individuais_atual = bases_individuais_atual[['Músicas']]

    return html.Div([
        dbc.Table.from_dataframe(bases_individuais_atual, striped=True, bordered=True, hover=True,color = 'primary',size = 'sm')
        ])

@app.callback(
    Output('tabela-segunda-func', 'children'),
    [Input('input-group-pesquisar-tenho', 'n_clicks')],
    [Input('dropdown-album-tenho', 'value')],
    *[Input(f'dropdown-{i}', 'value') for i in select_letras]
)
def update_tabela_segunda_func(botao, album_atual,*dropdown_values):
    if botao == 0:
        return dash.no_update
    if album_atual != 'Todos':
        bases_individuais_atual = bases_individuais[bases_individuais['album']==album_atual]
    else:
        bases_individuais_atual = bases_individuais

    for i in range(len(dropdown_values)):
        bases_individuais_atual = bases_individuais_atual[bases_individuais_atual[select_letras[i].lower()] <= int(dropdown_values[i])]
    bases_individuais_atual['Músicas'] = bases_individuais_atual['value']
    bases_individuais_atual = bases_individuais_atual.sort_values('prioridade').reset_index(drop = True).drop_duplicates(subset = 'ID').reset_index(drop = True)
    bases_individuais_atual = bases_individuais_atual.sort_values('ID').reset_index(drop = True)
    bases_individuais_atual = bases_individuais_atual[['Músicas']]

    return html.Div([
        dbc.Table.from_dataframe(bases_individuais_atual, striped=True, bordered=True, hover=True,color = 'primary',size = 'sm')
        ])

@app.callback(
    Output('tabela-terceira-func', 'children'),
    [Input('input-group-pesquisar_trechos', 'n_clicks')],
    [Input('dropdown-album-terceira', 'value')],
    [Input('dropdown-musica-terceira', 'value')],
    *[Input(f'dropdown-{i}', 'value') for i in select_letras]
)
def update_tabela_terceira_func(botao,album,musica_escolhida,*dropdown_values):


    if botao == 0:
        return dash.no_update
    lista_albuns = ['Debut', 'Fearless', 'Speak Now', 'Red', '1989', 'Reputation', 'Lover','folklore', 'evermore', 'Midnights']
    lista_cores = ['#00FFFF', '#FFFF00', '#800080', '#FF0000', '#ADD8E6', '#A9A9A9', '#FFC0CB', '#D3D3D3', '#7f3c10', '#526d85']
    index_cor = lista_albuns.index(album)
    cor = lista_cores[index_cor]
    titulo = musica_escolhida
    musica_escolhida = bases_individuais[bases_individuais['value'] == musica_escolhida]
    musica_escolhida = musica_escolhida.reset_index(drop = True)
    musica_escolhida = musica_escolhida['ID_combinacao'][0]


    query = "SELECT * FROM base_trechos_{};".format(int(musica_escolhida))
    db_connection = mysql.connector.connect(user='makethefriendshi',password='pedro100A',host='makethefriendshipbracelets.mysql.pythonanywhere-services.com',database='makethefriendshi$trechos_duplas')
    df_final_trechos = pd.read_sql(query, con=db_connection)
    df_filtragem = df_final_trechos
    for i in range(len(dropdown_values)-3):
        df_filtragem = df_filtragem[df_filtragem[select_letras[i].lower()] <= int(dropdown_values[i])]
    df_filtragem = df_filtragem.sort_values(by='trecho', key=lambda x: x.apply(len), ascending=False).reset_index(drop=True)
    df_filtragem = df_filtragem.drop_duplicates(subset='id', keep='first').reset_index(drop=True)

    meio = df_filtragem
    meio['colorir'] = meio['trecho']
    meio = df_filtragem[['id','colorir']]
    df_final_trechos = df_final_trechos.merge(meio, on='id', how='left')
    df_final_trechos['tamanho'] = df_final_trechos['trecho'].apply(len)
    df_final_trechos = df_final_trechos.sort_values(by='tamanho', ascending = False)
    df_final_trechos.drop_duplicates(subset='id',keep='first',inplace = True)
    df_final_trechos = df_final_trechos.sort_values(by='id').reset_index(drop=True)
    df_final_trechos = df_final_trechos[['trecho','colorir']]

    def highlight_text(row):
        full_text = row['trecho']
        highlight = row['colorir']

        if isinstance(highlight, str):
            parts = full_text.split(highlight)
            return html.P([
                parts[0],
                html.Span(highlight, style={"color": cor}),
                parts[1]
            ])
        else:
            return html.P(full_text)

    df_final_trechos['styled_text'] = df_final_trechos.apply(highlight_text, axis=1)

    return html.Div(children = [html.H3(titulo, style={'textAlign': 'center', 'color': 'white'}),html.Div([
                html.Div([
                    styled_text
                ])
                for styled_text in df_final_trechos['styled_text']
            ])])




@app.callback(
    Output('tabela-quarta-func', 'children'),
    [Input('input-group-pesquisar_otimizar', 'n_clicks')],
    *[Input(f'dropdown-{i}', 'value') for i in select_letras]
)
def update_tabela_quarta_func(botao,*dropdown_values):


    if botao == 0:
        return dash.no_update


    lista_letras = []
    for i in select_letras:
        lista_letras.append(i.lower())
    dropdown_values = [int(i) for i in dropdown_values]
    letras_input = pd.DataFrame([dropdown_values], columns=lista_letras)

    query = """SELECT * FROM base_duplas
    WHERE a <= {}
    AND b <= {}
    AND c <= {}
    AND d <= {}
    AND e <= {}
    AND f <= {}
    AND g <= {}
    AND h <= {}
    AND i <= {}
    AND j <= {}
    AND k <= {}
    AND l <= {}
    AND m <= {}
    AND n <= {}
    AND o <= {}
    AND p <= {}
    AND q <= {}
    AND r <= {}
    AND s <= {}
    AND t <= {}
    AND u <= {}
    AND v <= {}
    AND w <= {}
    AND x <= {}
    AND y <= {}
    AND z <= {}
    AND `1` <= {}
    AND `2` <= {}
    AND `4` <= {};
    """

    query = query.format(*dropdown_values)
    query = query.replace("#012", "\n")
    db_connection = mysql.connector.connect(user='makethefriendshi',password='pedro100A',host='makethefriendshipbracelets.mysql.pythonanywhere-services.com',database='makethefriendshi$trechos_duplas')

    base_duplas = pd.read_sql(query, con=db_connection)



    primeiro_df = otimizar_letras(letras_input,base_duplas,bases_individuais)
    count_ids = int((sum(primeiro_df.columns.str.startswith('ID')))/2)
    primeiro_df['Soma'] = primeiro_df.iloc[:, 2:31].sum(axis=1)
    primeiro_df = primeiro_df.sort_values(by = 'Soma', ascending = False).reset_index(drop=True)
    lista = []
    for i in range(1,count_ids):
        lista.append(primeiro_df['ID_{}'.format(i)][0])
    sliced_dfs = [primeiro_df.iloc[i:i+1] for i in range(0, len(primeiro_df), 1)][:20]
    listas_nomes = []
    count_ids = int((sum(primeiro_df.columns.str.startswith('ID')))/2)
    for j in sliced_dfs:
        lista = []
        intermediario = j.reset_index()
        if 'ID' in intermediario:
            intermediario['ID_1'] = intermediario['ID_combinacao']
        for i in range(1,count_ids+1):
            lista.append(intermediario['ID_{}'.format(i)][0])
        lista_atual = []
        for i in lista:
            lista_atual.append(bases_individuais[bases_individuais['ID_combinacao'] == i]['value'].reset_index()['value'][0])
        listas_nomes.append(lista_atual)
    listas_nomes = [sorted(inner_list) for inner_list in listas_nomes]
    unique_list = []
    [unique_list.append(item) for item in listas_nomes if item not in unique_list]
    listas_nomes = unique_list[:5]

    tables = []
    for i in range(len(listas_nomes)):
        tabela = criar_tabela(listas_nomes[i], i+1)
        tables.append(tabela)


    return html.Div(children = [html.H3('Sugestões', style={'textAlign': 'center', 'color': 'white'}),html.Div([
                html.Div([html.Div(table) for table in tables
])])])

@app.callback(
    Output('dropdown-musica-terceira', 'options'),
    Output('dropdown-musica-terceira', 'value'),
    Input('dropdown-album-terceira', 'value')
)
def update_song_options(selected_album):
    songs_in_album = bases_individuais[bases_individuais['album'] == selected_album]
    songs_in_album = songs_in_album[songs_in_album['Tipo'] == 'Original']['value']
    song_options = [{'label': song, 'value': song} for song in songs_in_album]

    default_song = song_options[0]['value']

    return song_options, default_song





@app.callback(
    Output('div-tenho-nao', 'style'),
    Input('radios', 'value')
)
def mostrar_segundo_radio(selected_radio):
    if selected_radio == 'titulos':
        return {
            "justify-content": "center",
            "align-items": "center", 'display': 'flex'}
    else:
        return {
            "justify-content": "center",
            "align-items": "center", 'display': 'none'}

@app.callback(
    Output('div-dropdowns', 'style'),
    Input('tenho_ou_nao', 'value'),
    Input('radios', 'value')
)
def mostrar_dropdowns(selected_radio,selected_radios):
    if selected_radio == 'tenho' or selected_radios != 'titulos':
        return {'display': 'block','textAlign': 'center'}
    else:
        return {'display': 'none'}





