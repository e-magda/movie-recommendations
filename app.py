# IMPORTS
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Display Setting (for urls cut at 50 signs)
pd.options.display.max_colwidth = 200


# DATA
df_30years = pd.read_csv("datasets/movies_30years.csv")
df_kids = pd.read_csv("datasets/movies_kids.csv")
df_family = pd.read_csv("datasets/movies_family.csv")
df_recent = pd.read_csv("datasets/movies_recent.csv")
df_horror = pd.read_csv("datasets/movies_horror.csv")
df_old_movies = pd.read_csv("datasets/movies_old.csv")

# Function to create a list with dictionaries of titles and tconst (movie IDs)
def list_titles(df):
    """The function creates a list of dictionaries to pass to the dropdown menu to choose a movie"""
    lst_tconst = list(df["tconst"])
    lst_title = list(df["title"])
    lst_options_films = []

    for i in range(len(lst_title)):
        dic_film = {"label": "", "value": ""}
        dic_film["label"] = lst_title[i]
        dic_film["value"] = lst_tconst[i]
        lst_options_films.append(dic_film)
    return lst_options_films


# Function to clean the list of production countries in the tables
def list_to_str(country):
    """The function takes a list of countries and returns a string without punctuation"""
    punctuation = '''[]'"'''
    for i in country:
        if i in punctuation:
            country = country.replace(i, "")
    return country


# Creating a dataframe and list with only tconst and titles for all movies for the dropdown menu sorted alphabetically
df_full = pd.DataFrame()
for df in (
    df_kids,
    df_family,
    df_recent,
    df_30years,
    df_horror,
    df_old_movies,
):
    df_full = pd.concat([df_full, df[["tconst", "title"]]])
df_full = df_full.drop_duplicates()
df_full_sorted = df_full.sort_values("title")
options_films = list_titles(df_full_sorted)


# FRONT-END
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.DARKLY],
)

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

main_page = html.Div(
    [
        dbc.Row(
            html.H1(
                "CINE CREUSE",
                style={
                    "position": "absolute",
                    "z-index": "1",
                    "textAlign": "center",
                    "marginTop": "20px",
                    "font-weight": "900",
                    "font-family": "bolder",
                },
            )
        ),
        dbc.Row(
            [
                html.Img(
                    src="assets/image-cine.jpeg",
                    style={
                        "position": "absolute",
                        "top": "0px",
                        "object-fit": "cover",
                        "width": "-webkit-fill-available",
                        "height": "300px",
                        "z-index": "0",
                        "opacity": "0.7",
                    },
                ),
            ],
            className="top-left",
        ),
        dbc.Container(
            [
                dbc.Row(
                    html.P(
                        "",
                        style={
                            "marginLeft": "80px",
                            "marginTop": "200px",
                            "font": "Garamond",
                        },
                    )
                ),
                dbc.Row([]),
                dbc.Row(
                    [
                        dbc.Container(
                            [
                                dbc.Button(
                                    "Accueil",
                                    id="btn-accueil",
                                    n_clicks=0,
                                    href="/",
                                    style={
                                        "background-color": "#375a5f",
                                        "border-color": "#375a5f",
                                    },
                                ),
                                dbc.Button(
                                    "Dernières sorties",
                                    id="btn-recent",
                                    n_clicks=0,
                                    href="/dernieres-sorties",
                                ),
                                dbc.Button(
                                    "Films cultes",
                                    id="btn-30-years",
                                    n_clicks=0,
                                    href="/films-cultes",
                                ),
                                dbc.Button(
                                    "En famille",
                                    id="btn-family",
                                    n_clicks=0,
                                    href="/en-famille",
                                ),
                                dbc.Button(
                                    "Jeunesse",
                                    id="btn-kids",
                                    n_clicks=0,
                                    href="/jeunesse",
                                ),
                                dbc.Button(
                                    "Horreur",
                                    id="btn-horror",
                                    n_clicks=0,
                                    href="/horreur",
                                ),
                                dbc.Button(
                                    "Ciné rétro",
                                    id="btn-old-movies",
                                    n_clicks=0,
                                    href="/cine-retro",
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="dropdown-options",
                                            options=options_films,
                                            style={
                                                "color": "#212121",
                                                "background-color": "#212121",
                                            },
                                            placeholder="Recherchez un film...",
                                        ),
                                    ],
                                    style={"width": "30%"},
                                ),
                            ],
                            className="d-grid gap-3 d-md-flex",
                            style={
                                "marginTop": "30px",
                                "marginBottom": "30px",
                                "justify-content": "flex-end",
                                "z-index": "2",
                            },
                        )
                    ]
                ),
                dbc.Row(id="selected-category"),
                dbc.Row(
                    [
                        html.H2(
                            "Cette semaine dans votre cinéma",
                            style={"marginTop": "30px", "marginBottom": "30px"},
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.P(
                                    "Dernières sorties",
                                    style={
                                        "marginBottom": "5px",
                                        "font-weight": "bold",
                                        "font-size": "larger",
                                    },
                                ),
                                html.P("Merc/Sam 20h", style={"marginBottom": "10px"}),
                                html.A(
                                    html.Img(
                                        src=np.array(
                                            df_recent[
                                                df_recent["tconst"] == "tt1160419"
                                            ]
                                        )[0, 8],
                                        width="auto",
                                        height=250,
                                    ),
                                    href="/tt1160419",
                                ),
                                html.P(
                                    np.array(
                                        df_recent[df_recent["tconst"] == "tt1160419"]
                                    )[0, 2],
                                    style={"marginTop": "15px", "font-weight": "bold"},
                                ),
                            ],
                            style={"textAlign": "center"},
                        ),
                        dbc.Col(
                            [
                                html.P(
                                    "Films cultes",
                                    style={
                                        "marginBottom": "5px",
                                        "font-weight": "bold",
                                        "font-size": "larger",
                                    },
                                ),
                                html.P("Dimanche 20h", style={"marginBottom": "10px"}),
                                html.A(
                                    html.Img(
                                        src=np.array(
                                            df_30years[
                                                df_30years["tconst"]
                                                == "tt0468569"
                                            ]
                                        )[0, 8],
                                        width="auto",
                                        height=250,
                                    ),
                                    href="/tt0468569",
                                ),
                                html.P(
                                    np.array(
                                        df_30years[
                                            df_30years["tconst"]
                                            == "tt0468569"
                                        ]
                                    )[0, 2],
                                    style={"marginTop": "15px", "font-weight": "bold"},
                                ),
                            ],
                            style={"textAlign": "center"},
                        ),
                        dbc.Col(
                            [
                                html.P(
                                    "En famille",
                                    style={
                                        "marginBottom": "5px",
                                        "font-weight": "bold",
                                        "font-size": "larger",
                                    },
                                ),
                                html.P(
                                    "Ven 20h/Dim 15h", style={"marginBottom": "10px"}
                                ),
                                html.A(
                                    html.Img(
                                        src=np.array(
                                            df_family[
                                                df_family["tconst"] == "tt0241527"
                                            ]
                                        )[0, 8],
                                        width="auto",
                                        height=250,
                                    ),
                                    href="/tt0241527",
                                ),
                                html.P(
                                    np.array(
                                        df_family[df_family["tconst"] == "tt0241527"]
                                    )[0, 2],
                                    style={"marginTop": "15px", "font-weight": "bold"},
                                ),
                            ],
                            style={"textAlign": "center"},
                        ),
                        dbc.Col(
                            [
                                html.P(
                                    "Jeunesse",
                                    style={
                                        "marginBottom": "5px",
                                        "font-weight": "bold",
                                        "font-size": "larger",
                                    },
                                ),
                                html.P("Mercredi 15h", style={"marginBottom": "10px"}),
                                html.A(
                                    html.Img(
                                        src=np.array(
                                            df_kids[df_kids["tconst"] == "tt0910970"]
                                        )[0, 8],
                                        width="auto",
                                        height=250,
                                    ),
                                    href="/tt0910970",
                                ),
                                html.P(
                                    np.array(df_kids[df_kids["tconst"] == "tt0910970"])[
                                        0, 2
                                    ],
                                    style={"marginTop": "15px", "font-weight": "bold"},
                                ),
                            ],
                            style={"textAlign": "center"},
                        ),
                        dbc.Col(
                            [
                                html.P(
                                    "Films d'horreur",
                                    style={
                                        "marginBottom": "5px",
                                        "font-weight": "bold",
                                        "font-size": "larger",
                                    },
                                ),
                                html.P("Samedi 15h", style={"marginBottom": "10px"}),
                                html.A(
                                    html.Img(
                                        src=np.array(
                                            df_horror[
                                                df_horror["tconst"] == "tt0081505"
                                            ]
                                        )[0, 8],
                                        width="auto",
                                        height=250,
                                    ),
                                    href="/tt0081505",
                                ),
                                html.P(
                                    np.array(
                                        df_horror[df_horror["tconst"] == "tt0081505"]
                                    )[0, 2],
                                    style={"marginTop": "15px", "font-weight": "bold"},
                                ),
                            ],
                            style={"textAlign": "center"},
                        ),
                        dbc.Col(
                            [
                                html.P(
                                    "Ciné rétro",
                                    style={
                                        "marginBottom": "5px",
                                        "font-weight": "bold",
                                        "font-size": "larger",
                                    },
                                ),
                                html.P("Jeudi 20h", style={"marginBottom": "10px"}),
                                html.A(
                                    html.Img(
                                        src=np.array(
                                            df_old_movies[
                                                df_old_movies["tconst"] == "tt0068646"
                                            ]
                                        )[0, 8],
                                        width="auto",
                                        height=250,
                                    ),
                                    href="/tt0068646",
                                ),
                                html.P(
                                    np.array(
                                        df_old_movies[
                                            df_old_movies["tconst"] == "tt0068646"
                                        ]
                                    )[0, 2],
                                    style={"marginTop": "15px", "font-weight": "bold"},
                                ),
                            ],
                            style={"textAlign": "center"},
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        html.Hr(
                            style={"marginTop": "30px", "marginBottom": "20px","height": "3px"},
                        ),
                        html.Img(
                            src="assets/slide_planning.jpg", style={"width": "1200px", "margin-left": "70px", "margin-top": "30px"}
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(width=7
                               ),
                        dbc.Col(
                            [
                                html.P(
                                    "",
                                    style={
                                        "marginLeft": "80px",
                                        "marginTop": "100px",
                                        "font": "Garamond",
                                    },
                                ),
                                html.P(
                                    "Par les 4 Pandastiques, 2021",
                                    style={
                                        "marginTop": "60px",
                                        "marginBottom": "30px",
                                        "marginLeft": "80px",
                                    },
                                ),
                            ], width=3
                        ),
                        dbc.Col(
                            html.Img(
                                    src="assets/logo-pandastic.png",
                                    style={"marginTop": "40px",
                                           "width": "80px"}
                            )
                        )
                    ]
                )
            ]
        )
    ]
)


page_movie_layout = html.Div(
    [
        dbc.Row(
            html.H1(
                "CINE CREUSE",
                style={
                    "position": "absolute",
                    "z-index": "1",
                    "textAlign": "center",
                    "marginTop": "20px",
                    "font-weight": "900",
                    "font-family": "bolder",
                },
            )
        ),
        dbc.Row(
            [
                html.Img(
                    src="assets/image-cine.jpeg",
                    style={
                        "position": "absolute",
                        "top": "0px",
                        "object-fit": "cover",
                        "width": "-webkit-fill-available",
                        "height": "300px",
                        "z-index": "0",
                        "opacity": "0.7",
                    },
                ),
            ],
            className="top-left",
        ),
        dbc.Container(
            [
                dbc.Row(
                    html.P(
                        "",
                        style={
                            "marginLeft": "80px",
                            "marginTop": "200px",
                            "font": "Garamond",
                        },
                    )
                ),
                dbc.Row([]),
                dbc.Row(
                    [
                        dbc.Container(
                            [
                                dbc.Button(
                                    "Accueil",
                                    id="btn-accueil",
                                    n_clicks=0,
                                    href="/",
                                    style={
                                        "background-color": "#375a5f",
                                        "border-color": "#375a5f",
                                    },
                                ),
                                dbc.Button(
                                    "Dernières sorties",
                                    id="btn-recent",
                                    n_clicks=0,
                                    href="/dernieres-sorties",
                                ),
                                dbc.Button(
                                    "Films cultes",
                                    id="btn-30-years",
                                    n_clicks=0,
                                    href="/films-cultes",
                                ),
                                dbc.Button(
                                    "En famille",
                                    id="btn-family",
                                    n_clicks=0,
                                    href="/en-famille",
                                ),
                                dbc.Button(
                                    "Jeunesse",
                                    id="btn-kids",
                                    n_clicks=0,
                                    href="/jeunesse",
                                ),
                                dbc.Button(
                                    "Horreur",
                                    id="btn-horror",
                                    n_clicks=0,
                                    href="/horreur",
                                ),
                                dbc.Button(
                                    "Ciné rétro",
                                    id="btn-old-movies",
                                    n_clicks=0,
                                    href="/cine-retro",
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="dropdown-options-2",
                                            options=options_films,
                                            style={
                                                "color": "#212121",
                                                "background-color": "#212121",
                                            },
                                            placeholder="Recherchez un film...",
                                        ),
                                    ],
                                    style={"width": "30%"},
                                ),
                            ],
                            className="d-grid gap-3 d-md-flex",
                            style={
                                "marginTop": "30px",
                                "marginBottom": "30px",
                                "justify-content": "flex-end",
                                "z-index": "2",
                            },
                        )
                    ]
                ),
                dbc.Row(id="selected-movie"),
            ]
        ),
    ]
)


# Callback function to get selected movie (dropdown or category) informations in database and display them
@app.callback(
    Output("selected-category", "children"), Input("dropdown-options", "value")
)
def infos_movie(value):
    if value is None:
        return None

    else:
        if value in df_kids["tconst"].values:
            df_infos = df_kids.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance pour enfants."

        elif value in df_family["tconst"].values:
            df_infos = df_family.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance pour familles."

        elif value in df_30years["tconst"].values:
            df_infos = df_30years.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance de films cultes."

        elif value in df_recent["tconst"].values:
            df_infos = df_recent.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance des dernières sorties."

        elif value in df_horror["tconst"].values:
            df_infos = df_horror.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance horreur."

        elif value in df_old_movies["tconst"].values:
            df_infos = df_old_movies.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance de ciné rétro."

        infos_film = np.array(df_infos[df_infos["tconst"] == value])
        intro = "Votre film"

    tconst = infos_film[0, 1]
    title = infos_film[0, 2]
    genre1 = infos_film[0, 3]
    numVotes = int(infos_film[0, 4])
    startYear = int(infos_film[0, 5])
    runtimeMinutes = int(infos_film[0, 6])
    averageRating = infos_film[0, 7]
    url = infos_film[0, 8]
    pays_prod = list_to_str(infos_film[0, 9])
    synopsis = infos_film[0, 10]
    reco1 = infos_film[0, 11]
    reco2 = infos_film[0, 12]
    reco3 = infos_film[0, 13]
    reco4 = infos_film[0, 14]
    url_trailer = infos_film[0, 15]

    recos_img = []
    recos_title = []
    for reco in (reco1, reco2, reco3, reco4):
        infos_reco = np.array(df_infos[df_infos["tconst"] == reco])
        if infos_reco.shape[0] != 0:
            tconst_reco = infos_reco[0, 1]
            title_reco = infos_reco[0, 2]
            url_reco = infos_reco[0, 8]
            recos_title.append(html.P(title_reco))
            recos_img.append(
                html.A(
                    html.Img(src=url_reco, width=165, height="auto"),
                    href="/" + tconst_reco,
                )
            )

    selection_layout = (
        dbc.Row(html.H2("À l'affiche", style={"marginTop": "30px"})),
        dbc.Row(html.H4(intro, style={"marginTop": "10px", "marginBottom": "30px"})),
        dbc.Row(
            [
                dbc.Col(
                    html.A(
                        html.Img(src=url, width="auto", height=280), href="/" + tconst
                    ),
                    width=2,
                ),
                dbc.Col(
                    [
                        html.H3(title, style={"marginBottom": "15px"}),
                        html.P(
                            f"Date de sortie : {startYear}",
                            style={"marginBottom": "5px"},
                        ),
                        html.P(f"Genre : {genre1}", style={"marginBottom": "5px"}),
                        html.P(
                            f"Pays de production : {pays_prod}",
                            style={"marginBottom": "5px"},
                        ),
                        html.P(
                            f"Temps : {(runtimeMinutes)} min",
                            style={"marginBottom": "15px"},
                        ),
                        html.P(
                            f"Statistiques IMDb : note moyenne de {averageRating}/10 pour {numVotes} votes",
                            style={"marginBottom": "15px"},
                        ),
                        html.P(synopsis, style={"marginBottom": "30px"}),
                    ],
                    width=5,
                ),
                dbc.Col([html.Embed(src=url_trailer, width=400, height=280)], width=5),
            ]
        ),
        dbc.Row(
            [
                html.H4(
                    "Vous pourriez aussi aimer",
                    style={"marginTop": "30px", "marginBottom": "30px"},
                ),
                dbc.Row([dbc.Col(i) for i in recos_img], style={"textAlign": "center"}),
                dbc.Row(
                    [dbc.Col(j) for j in recos_title],
                    style={
                        "textAlign": "center",
                        "marginTop": "15px",
                        "font-weight": "bold",
                    },
                ),
            ]
        ),
        html.Hr(style={"marginTop": "30px"}),
    )

    return selection_layout


# Callback function to get selected movie (dropdown or category) informations in database and display them
@app.callback(
    Output("selected-movie", "children"), Input("dropdown-options-2", "value")
)
def infos_movie(value):
    if value is None:
        return None

    else:
        if value in df_kids["tconst"].values:
            df_infos = df_kids.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance pour enfants."

        elif value in df_family["tconst"].values:
            df_infos = df_family.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance pour familles."

        elif value in df_30years["tconst"].values:
            df_infos = df_30years.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance de films cultes."

        elif value in df_recent["tconst"].values:
            df_infos = df_recent.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance des dernières sorties."

        elif value in df_horror["tconst"].values:
            df_infos = df_horror.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance horreur."

        elif value in df_old_movies["tconst"].values:
            df_infos = df_old_movies.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance de ciné rétro."

        infos_film = np.array(df_infos[df_infos["tconst"] == value])
        intro = "Votre film"

    tconst = infos_film[0, 1]
    title = infos_film[0, 2]
    genre1 = infos_film[0, 3]
    numVotes = int(infos_film[0, 4])
    startYear = int(infos_film[0, 5])
    runtimeMinutes = int(infos_film[0, 6])
    averageRating = infos_film[0, 7]
    url = infos_film[0, 8]
    pays_prod = list_to_str(infos_film[0, 9])
    synopsis = infos_film[0, 10]
    reco1 = infos_film[0, 11]
    reco2 = infos_film[0, 12]
    reco3 = infos_film[0, 13]
    reco4 = infos_film[0, 14]
    url_trailer = infos_film[0, 15]

    recos_img = []
    recos_title = []
    for reco in (reco1, reco2, reco3, reco4):
        infos_reco = np.array(df_infos[df_infos["tconst"] == reco])
        if infos_reco.shape[0] != 0:
            tconst_reco = infos_reco[0, 1]
            title_reco = infos_reco[0, 2]
            url_reco = infos_reco[0, 8]
            recos_title.append(html.P(title_reco))
            recos_img.append(
                html.A(
                    html.Img(src=url_reco, width=165, height="auto"),
                    href="/" + tconst_reco,
                )
            )

    selection_layout = (
        dbc.Row(html.H2("À l'affiche", style={"marginTop": "30px"})),
        dbc.Row(html.H4(intro, style={"marginTop": "10px", "marginBottom": "30px"})),
        dbc.Row(
            [
                dbc.Col(
                    html.A(
                        html.Img(src=url, width="auto", height=280), href="/" + tconst
                    ),
                    width=2,
                ),
                dbc.Col(
                    [
                        html.H3(title, style={"marginBottom": "15px"}),
                        html.P(
                            f"Date de sortie : {startYear}",
                            style={"marginBottom": "5px"},
                        ),
                        html.P(f"Genre : {genre1}", style={"marginBottom": "5px"}),
                        html.P(
                            f"Pays de production : {pays_prod}",
                            style={"marginBottom": "5px"},
                        ),
                        html.P(
                            f"Temps : {(runtimeMinutes)} min",
                            style={"marginBottom": "15px"},
                        ),
                        html.P(
                            f"Statistiques IMDb : note moyenne de {averageRating}/10 pour {numVotes} votes",
                            style={"marginBottom": "15px"},
                        ),
                        html.P(synopsis, style={"marginBottom": "30px"}),
                    ],
                    width=5,
                ),
                dbc.Col([html.Embed(src=url_trailer, width=400, height=280)], width=5),
            ]
        ),
        dbc.Row(
            [
                html.H4(
                    "Vous pourriez aussi aimer",
                    style={"marginTop": "30px", "marginBottom": "30px"},
                ),
                # html.Div(recos, className="d-grid gap-5 d-md-flex",)
                dbc.Row([dbc.Col(i) for i in recos_img], style={"textAlign": "center"}),
                dbc.Row(
                    [dbc.Col(j) for j in recos_title],
                    style={
                        "textAlign": "center",
                        "marginTop": "15px",
                        "font-weight": "bold",
                    },
                ),
            ]
        ),
        html.Hr(style={"marginTop": "30px"}),
    )

    return selection_layout


# Callback function to display the selected page
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname.startswith("/tt"):
        value = "".join(car for car in pathname if car != "/")

        if value in df_kids["tconst"].values:
            df_infos = df_kids.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance pour enfants."

        elif value in df_family["tconst"].values:
            df_infos = df_family.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance pour familles."

        elif value in df_30years["tconst"].values:
            df_infos = df_30years.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance de films cultes."

        elif value in df_recent["tconst"].values:
            df_infos = df_recent.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance des dernières sorties."

        elif value in df_horror["tconst"].values:
            df_infos = df_horror.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance horreur."

        elif value in df_old_movies["tconst"].values:
            df_infos = df_old_movies.copy()
            seance = "Vous pouvez programmer ce film lors d'une séance de ciné rétro."

        infos_film = np.array(df_infos[df_infos["tconst"] == value])
        intro = "Votre film"

        tconst = infos_film[0, 1]
        title = infos_film[0, 2]
        genre1 = infos_film[0, 3]
        numVotes = int(infos_film[0, 4])
        startYear = int(infos_film[0, 5])
        runtimeMinutes = int(infos_film[0, 6])
        averageRating = infos_film[0, 7]
        url = infos_film[0, 8]
        pays_prod = list_to_str(infos_film[0, 9])
        synopsis = infos_film[0, 10]
        reco1 = infos_film[0, 11]
        reco2 = infos_film[0, 12]
        reco3 = infos_film[0, 13]
        reco4 = infos_film[0, 14]
        url_trailer = infos_film[0, 15]

        recos_img = []
        recos_title = []
        for reco in (reco1, reco2, reco3, reco4):
            infos_reco = np.array(df_infos[df_infos["tconst"] == reco])
            if infos_reco.shape[0] != 0:
                tconst_reco = infos_reco[0, 1]
                title_reco = infos_reco[0, 2]
                url_reco = infos_reco[0, 8]
                recos_title.append(html.P(title_reco))
                recos_img.append(
                    html.A(
                        html.Img(src=url_reco, width=165, height="auto"),
                        href="/" + tconst_reco,
                    )
                )

        return page_movie_layout, dbc.Container(
            [
                dbc.Row(
                    html.H3(intro, style={"marginTop": "30px", "marginBottom": "30px"})
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.A(
                                html.Img(src=url, width="auto", height=280),
                                href="/" + tconst,
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            [
                                html.H3(title, style={"marginBottom": "15px"}),
                                html.P(
                                    f"Date de sortie : {startYear}",
                                    style={"marginBottom": "5px"},
                                ),
                                html.P(
                                    f"Genre : {genre1}", style={"marginBottom": "5px"}
                                ),
                                html.P(
                                    f"Pays de production : {pays_prod}",
                                    style={"marginBottom": "5px"},
                                ),
                                html.P(
                                    f"Temps : {(runtimeMinutes)} min",
                                    style={"marginBottom": "15px"},
                                ),
                                html.P(
                                    f"Statistiques IMDb : note moyenne de {averageRating}/10 pour {numVotes} votes",
                                    style={"marginBottom": "15px"},
                                ),
                                html.P(synopsis, style={"marginBottom": "30px"}),
                            ],
                            width=5,
                        ),
                        dbc.Col(
                            [html.Embed(src=url_trailer, width=400, height=280)],
                            width=5,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        html.H4(
                            "Vous pourriez aussi aimer",
                            style={"marginTop": "30px", "marginBottom": "30px"},
                        ),
                        dbc.Row(
                            [dbc.Col(i) for i in recos_img],
                            style={"textAlign": "center"},
                        ),
                        dbc.Row(
                            [dbc.Col(j) for j in recos_title],
                            style={
                                "textAlign": "center",
                                "marginTop": "15px",
                                "font-weight": "bold",
                            },
                        ),
                    ]
                ),
                html.Hr(style={"marginTop": "30px"}),
            ]
        )

    else:
        if pathname == "/":
            return main_page

        elif pathname == "/dernieres-sorties":
            df_infos = df_recent.copy()
            infos_film = np.array(df_infos[df_infos["tconst"] == "tt1160419"])
            intro = "Dernière sortie : mercredi et samedi soir"

        elif pathname == "/films-cultes":
            df_infos = df_30years.copy()
            infos_film = np.array(df_infos[df_infos["tconst"] == "tt0468569"])
            intro = "Film culte : dimanche soir"

        elif pathname == "/jeunesse":
            df_infos = df_kids.copy()
            infos_film = np.array(df_infos[df_infos["tconst"] == "tt0910970"])
            intro = "Jeunesse : mercredi après-midi"

        elif pathname == "/en-famille":
            df_infos = df_family.copy()
            infos_film = np.array(df_infos[df_infos["tconst"] == "tt0241527"])
            intro = "En famille : vendredi et dimanche"

        elif pathname == "/horreur":
            df_infos = df_horror.copy()
            infos_film = np.array(df_infos[df_infos["tconst"] == "tt0081505"])
            intro = "Horreur : samedi après-midi"

        elif pathname == "/cine-retro":
            df_infos = df_old_movies.copy()
            infos_film = np.array(df_infos[df_infos["tconst"] == "tt0068646"])
            intro = "Ciné rétro : jeudi soir"

        else:
            return main_page

        tconst = infos_film[0, 1]
        title = infos_film[0, 2]
        genre1 = infos_film[0, 3]
        numVotes = int(infos_film[0, 4])
        startYear = int(infos_film[0, 5])
        runtimeMinutes = int(infos_film[0, 6])
        averageRating = infos_film[0, 7]
        url = infos_film[0, 8]
        pays_prod = list_to_str(infos_film[0, 9])
        synopsis = infos_film[0, 10]
        reco1 = infos_film[0, 11]
        reco2 = infos_film[0, 12]
        reco3 = infos_film[0, 13]
        reco4 = infos_film[0, 14]
        url_trailer = infos_film[0, 15]

        recos_img = []
        recos_title = []
        for reco in (reco1, reco2, reco3, reco4):
            infos_reco = np.array(df_infos[df_infos["tconst"] == reco])
            if infos_reco.shape[0] != 0:
                tconst_reco = infos_reco[0, 1]
                title_reco = infos_reco[0, 2]
                url_reco = infos_reco[0, 8]
                recos_title.append(html.P(title_reco))
                recos_img.append(
                    html.A(
                        html.Img(src=url_reco, width=165, height="auto"),
                        href="/" + tconst_reco,
                    )
                )

        return page_movie_layout, dbc.Container(
            [
                dbc.Row(html.H2("À l'affiche", style={"marginTop": "30px"})),
                dbc.Row(
                    html.H4(intro, style={"marginTop": "10px", "marginBottom": "30px"})
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.A(
                                html.Img(src=url, width="auto", height=280),
                                href="/" + tconst,
                            ),
                            width=2,
                        ),
                        dbc.Col(
                            [
                                html.H3(title, style={"marginBottom": "15px"}),
                                html.P(
                                    f"Date de sortie : {startYear}",
                                    style={"marginBottom": "5px"},
                                ),
                                html.P(
                                    f"Genre : {genre1}", style={"marginBottom": "5px"}
                                ),
                                html.P(
                                    f"Pays de production : {pays_prod}",
                                    style={"marginBottom": "5px"},
                                ),
                                html.P(
                                    f"Temps : {(runtimeMinutes)} min",
                                    style={"marginBottom": "15px"},
                                ),
                                html.P(
                                    f"Statistiques IMDb : note moyenne de {averageRating}/10 pour {numVotes} votes",
                                    style={"marginBottom": "15px"},
                                ),
                                html.P(synopsis, style={"marginBottom": "30px"}),
                            ],
                            width=5,
                        ),
                        dbc.Col(
                            [html.Embed(src=url_trailer, width=400, height=280)],
                            width=5,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        html.H4(
                            "Vous pourriez aussi aimer",
                            style={"marginTop": "30px", "marginBottom": "30px"},
                        ),
                        dbc.Row(
                            [dbc.Col(i) for i in recos_img],
                            style={"textAlign": "center"},
                        ),
                        dbc.Row(
                            [dbc.Col(j) for j in recos_title],
                            style={
                                "textAlign": "center",
                                "marginTop": "15px",
                                "font-weight": "bold",
                            },
                        ),
                    ]
                ),
                html.Hr(style={"marginTop": "30px"}),
            ]
        )

if __name__ == '__main__':
    app.run_server(debug=True)

# Code to run app in jupyter lab 
# app.run_server(mode="external", port=8080)
