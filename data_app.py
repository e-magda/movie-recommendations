# IMPORTS
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output 
import dash_bootstrap_components as dbc
import random


# FRONT-END
app = Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Content of the index_page with links to our 2 pages (data, recommendations)
index_page = dbc.Container([
    html.Div([
        
        dbc.Row([
            
            dbc.Col(children=[
                html.H1("Une analyse du cinéma", style={'textAlign': 'center', 'marginTop': '30px', 'marginLeft': '160px'}),
                html.H3("par les Pandastic Four", style={'textAlign': 'center', 'marginLeft': '160px'})],
                    width=10,
                   ),
            
            dbc.Col(html.Img(src='assets/logo-pandastic.png', width=100, height='auto'), 
                    style={'textAlign': 'center', 'marginTop': '30px', 'marginBottom':'60px'}
                   )                   
        ]),
        
        dbc.Row([
            html.Img(src='assets/pellicule-1.png', style={'position': 'absolute','top': '0px', 'z-index':'0', 'width':'1200px'}),
            
            dbc.Row([
                dcc.Link(html.Button('Exploration des données cinématographiques', id='btn-nclicks-1',
                style={'position':'absolute','padding': '40px', 'marginTop':'90px', 'margin-bottom': '20px', 'marginLeft':'400px', 'background': 'white',
                       'padding-top': '80px', 'padding-bottom': '80px', 'border': '2px solid rgb(169, 190, 194)', 'border-radius':'20px', 'z-index': '5'}), href='http://127.0.0.1:8050/page-1',
                        ), 
            ]),
            
            dbc.Row(style={'height':'400px'}),
            
            dbc.Row([
                html.A(html.Button('Application de recommandations de films', id='btn-nclicks-2',
                style={'position':'absolute', 'padding': '40px', 'marginTop':'80px', 'margin-bottom': '20px', 'marginLeft':'400px', 'background': 'white',
                       'padding-top': '80px', 'padding-bottom': '80px', 'border': '2px solid rgb(169, 190, 194)', 'border-radius':'20px', 'z-index': '5'}), href='http://127.0.0.1:8080/',
                       target="_blank"
                        ),
            ])
        ])
    ])
])

# Content of page 1 with 4 tabs for data exploration
page_1_layout = dbc.Container([
    html.Div([
        dbc.Row([
            
            dbc.Col(children=[
                html.H1("Une analyse du cinéma", style={'textAlign': 'center', 'marginTop': '30px'}),
                html.H3("par les Pandastic Four", style={'textAlign': 'center'})],
                    width=10,
                   ),
            
            dbc.Col(html.Img(src='assets/logo-pandastic.png', width=100, height='auto'), style={'textAlign': 'center', 'marginTop': '30px'}
                   )
                   
        ])
    ]),

        html.Div(id='page-1-content'),
        html.Br(),
        html.A('Voir planning', href='http://127.0.0.1:8080/', target="_blank"),
        html.Br(),
        dcc.Link('Retour à l\'accueil', href='/'),

        html.Hr(),
        
        dcc.Tabs(
            children=[
                dcc.Tab(label="Exploration des données du cinéma", value="kpi_cinema"),
                dcc.Tab(label="Analyse cinématographique de la Creuse", value="kpi_creuse"),
                dcc.Tab(label="Statistiques affinées", value="kpi_detailed"),
                dcc.Tab(label="Anecdotes du cinéma", value="fun_facts"),

            ],
            id="tabs",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)

@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value")
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and returns the tab content depending on what the value of 'active_tab' is.
    """
    if active_tab == "kpi_cinema":
        return dbc.Row(
            [
                dbc.Col(html.Embed(src="https://chart-studio.plotly.com/~emi-magda/20.embed", width=1200, height=500)),
            ]
        ), dbc.Row(
            [
                dbc.Col(html.Embed(src="https://chart-studio.plotly.com/~emi-magda/15.embed", width=1200, height=500)),
            ]
        ), dbc.Row(
            [
                dbc.Col(html.Embed(src="https://chart-studio.plotly.com/~emi-magda/13.embed", width=1200, height=500)),
            ]
        )
    
    elif active_tab == "kpi_creuse":
        return dbc.Row([
            html.Img(src = 'assets/creuse-infos.png', style={'marginBottom': '30px'})
               
        ]), dbc.Row(
            [
                dbc.Col(children =[
                    html.P("Géographie du cinéma - Creuse"),
                    html.Embed(src="https://despro-cnc.maps.arcgis.com/apps/MapSeries/index.html?appid=a0a1e4f8ca7a44c1a2b175cb3291a17a", width=600, height=400)
                ], width=6
                       ),
                dbc.Col(children=[
                    html.A("Géographie du cinéma - Creuse",
                        href="https://www.cnc.fr/cinema/etudes-et-rapports/statistiques/datavisualisation-la-geographie-du-cinema",
                             target='_blank', style={'marginBottom': '30px'}
                       ),
                html.Img(src="assets/stats-creuse.png", width=600, height=400)
            ], width=6)
            ])
                
    elif active_tab == "kpi_detailed":
        return dbc.Row(
            children=[
                html.H3("Notre sélection de films pour votre cinéma", style={'marginTop': '30px'}),
                html.H4("Les dernières sorties", style={'marginTop': '30px'})
            ]
        ), dbc.Row(
            [
                dbc.Col(html.Embed(src="https://chart-studio.plotly.com/~emi-magda/60.embed", width=600, height=400), width=6),
                dbc.Col(html.Embed(src="https://chart-studio.plotly.com/~emi-magda/66.embed", width=600, height=400), width=6)
            ]
        ), dbc.Row(
            html.H4("Les meilleurs films des 30 dernières années", style={'marginTop': '30px'})
            
        ), dbc.Row(
            [
                dbc.Col(html.Embed(src="https://chart-studio.plotly.com/~emi-magda/68.embed", width=600, height=400), width=6),
                dbc.Col(html.Embed(src="https://chart-studio.plotly.com/~emi-magda/70.embed", width=600, height=400), width=6)  
            ]
        ), dbc.Row(
            html.H4("Des classiques à regarder en famille", style={'marginTop': '30px'})
            
        ), dbc.Row(
            [
                dbc.Col(html.Embed(src="https://chart-studio.plotly.com/~emi-magda/23.embed", width=600, height=400), width=6),
                dbc.Col(html.Embed(src="https://chart-studio.plotly.com/~emi-magda/30.embed", width=600, height=400), width=6)
               
            ]
        ), dbc.Row(
            html.H4("Des films pour les plus petits", style={'marginTop': '30px'})
            
        ), dbc.Row(
            [
                dbc.Col(html.Embed(src="https://chart-studio.plotly.com/~emi-magda/73.embed", width=600, height=400), width=6),
                dbc.Col(html.Embed(src="https://chart-studio.plotly.com/~emi-magda/76.embed", width=600, height=400), width=6)
            ]
        ), dbc.Row(
            html.H4("Pour faire frissonner votre audience", style={'marginTop': '30px'})
            
        ), dbc.Row(
            [
                dbc.Col(html.Embed(src="https://chart-studio.plotly.com/~emi-magda/50.embed", width=600, height=400), width=6),
                dbc.Col(html.Embed(src="https://chart-studio.plotly.com/~emi-magda/54.embed", width=600, height=400), width=6)
            ]
        ), dbc.Row(
            html.H4("Pour revivre le cinéma d'époque", style={'marginTop': '30px'})
            
        ), dbc.Row(
            [
                dbc.Col(html.Embed(src="https://chart-studio.plotly.com/~emi-magda/56.embed", width=600, height=400), width=6),
                dbc.Col(html.Embed(src="https://chart-studio.plotly.com/~emi-magda/58.embed", width=600, height=400), width=6)
            ]
        )
    
    elif active_tab == "fun_facts":
        return dbc.Row(
                html.H3("Quelques anecdotes sur le cinéma", style={'marginTop': '30px', 'marginBottom': '30px'})
            
        ), dbc.Row(
            [
                dbc.Col(
                    children = [
                        html.H4("Le saviez-vous ?", style={'margin-bottom':'30px'}),
                        html.P(f""""{random.choice(list(open('datasets/Anecdotes.txt')))}" """),
                        html.P(f"Source: Huffington Post, 51 anecdotes sur le cinéma que vous ne connaissez certainement pas, 27/08/2013",
                              style={'font-size':'11px'})
                    ],
                    width=5
        ),
                dbc.Col(
                    children=[
                        html.H4("Nos données sans filtre...", style={'margin-bottom':'30px'}),
                        html.Img(src="assets/richard.png", width=700)
                    ],
                    width=7   
        )
            ])


# Callback function to display the wanted page (page 1 and page 2 are not connected at the moment)
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    if pathname == 'http://127.0.0.1:8080/':
        return page_2_layout
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)

# Launching app in jupyter lab
# app.run_server(mode='external')