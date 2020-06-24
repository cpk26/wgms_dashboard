import plotly.graph_objects as go
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Data Import
df_combined = pd.read_pickle("wgms_combined")
df_thickness = pd.read_pickle("wgms_thickness")
df_massbalance = pd.read_pickle("wgms_massbalance")
df_front = pd.read_pickle("wgms_front")

# Default selection is Mer De Glace, WGMS_ID = 353
mer_de_glace = 353

# Satellite Map
def update_satellite_map():

    data = go.Scattermapbox(
        lon=df_combined["LONGITUDE"],
        lat=df_combined["LATITUDE"],
        customdata=df_combined["WGMS_ID"],
        mode="markers",
        marker=go.scattermapbox.Marker(size=8),
    )
    layout = dict(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=0,
        mapbox_center_lon=0,
        mapbox_zoom=0,
        autosize=True,
        height=300,
        margin=dict(l=0, r=0, b=0, t=0, pad=50),
    )

    figure = go.Figure(data=data, layout=layout)
    return figure


# Dash App

app = dash.Dash(
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://codepen.io/chriddyp/pen/bWLwgP.css",
    ]
)

# Layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            "World Glacier Monitoring Service", className="text-center"
                        ),
                        html.H5("Data Explorer", className="text-center"),
                    ],
                    md=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            [html.H3("XXk"), "Glaciers"],
                                            className="mini_container",
                                        ),
                                    ],
                                    width=3,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [html.H3("19XX"), "Oldest Record"],
                                        className="mini_container",
                                    ),
                                    width=3,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [html.H3("XXX+"), "Contributors"],
                                        className="mini_container",
                                    ),
                                    width=3,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [html.H3("XX"), "Countries"],
                                        className="mini_container",
                                    ),
                                    width=3,
                                ),
                            ],
                        ),
                        dbc.Row(
                            dbc.Col(
                                html.Div(
                                    [
                                        html.H5(
                                            "Satellite Overview",
                                            className="text-center",
                                        ),
                                        dcc.Graph(
                                            figure=update_satellite_map(), id="mapbox"
                                        ),
                                    ],
                                    className="mini_container satellite_container",
                                ),
                                width=12,
                            ),
                        ),
                    ],
                    md=8,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.P("Filter by earliest measurement:"),
                                            dcc.Slider(
                                                id="my-slider",
                                                min=1850,
                                                max=2020,
                                                step=1,
                                                value=2020,
                                                marks={
                                                    1850: "1850",
                                                    1900: "1900",
                                                    1950: "1950",
                                                    2000: "2000",
                                                },
                                            ),
                                        ],
                                        className="selection_item",
                                    ),
                                    html.Div(
                                        [
                                            html.P("Filter by years of data:"),
                                            dcc.Slider(
                                                id="my-slider2",
                                                min=0,
                                                max=10,
                                                step=1,
                                                value=2020,
                                                marks={
                                                    0: "0",
                                                    2: "2",
                                                    4: "4",
                                                    6: "6",
                                                    8: "8",
                                                    10: "10+",
                                                },
                                            ),
                                        ],
                                        className="selection_item",
                                    ),
                                    html.Div(
                                        [
                                            html.P("Filter by Primary Classification:"),
                                            dcc.Dropdown(
                                                options=[
                                                    {
                                                        "label": "Miscellaneous",
                                                        "value": "0",
                                                    },
                                                    {
                                                        "label": "Continental ice sheet",
                                                        "value": "1",
                                                    },
                                                    {
                                                        "label": "Ice Field",
                                                        "value": "2",
                                                    },
                                                    {"label": "Ice Cap", "value": "3"},
                                                    {
                                                        "label": "Outlet Glacier",
                                                        "value": "4",
                                                    },
                                                    {
                                                        "label": "Valley Glacier",
                                                        "value": "5",
                                                    },
                                                    {
                                                        "label": "Mountain glacier ",
                                                        "value": "6",
                                                    },
                                                    {
                                                        "label": "Glacieret and snowfield",
                                                        "value": "7",
                                                    },
                                                    {
                                                        "label": "Ice Shelf",
                                                        "value": "8",
                                                    },
                                                    {
                                                        "label": "Rock Glacier",
                                                        "value": "9",
                                                    },
                                                ],
                                                multi=True,
                                                value="None",
                                            ),
                                        ],
                                        className="selection_item",
                                    ),
                                    html.Div(
                                        [
                                            html.P("Filter by Form:"),
                                            dcc.Dropdown(
                                                options=[
                                                    {
                                                        "label": "Miscellaneous",
                                                        "value": "0",
                                                    },
                                                    {
                                                        "label": "Compound Basins",
                                                        "value": "1",
                                                    },
                                                    {
                                                        "label": "Compound Basin",
                                                        "value": "2",
                                                    },
                                                    {
                                                        "label": "Simple Basin",
                                                        "value": "3",
                                                    },
                                                    {"label": "Circque", "value": "4"},
                                                    {"label": "Niche", "value": "5"},
                                                    {"label": "Crater", "value": "6",},
                                                    {
                                                        "label": "Ice Apron",
                                                        "value": "7",
                                                    },
                                                    {"label": "Group", "value": "8"},
                                                    {"label": "Remnant", "value": "9"},
                                                ],
                                                multi=True,
                                                value="None",
                                            ),
                                        ],
                                        className="selection_item",
                                    ),
                                    html.Div(
                                        [
                                            html.P(
                                                "Filter by Frontal Characteristics:"
                                            ),
                                            dcc.Dropdown(
                                                options=[
                                                    {
                                                        "label": "Miscellaneous",
                                                        "value": "0",
                                                    },
                                                    {
                                                        "label": "Piedmont",
                                                        "value": "1",
                                                    },
                                                    {
                                                        "label": "Expanded Foot",
                                                        "value": "2",
                                                    },
                                                    {"label": "Lobed", "value": "3"},
                                                    {"label": "Calving", "value": "4"},
                                                    {
                                                        "label": "Coalescing, non-contributing",
                                                        "value": "5",
                                                    },
                                                    {
                                                        "label": "Irregular, clean ice",
                                                        "value": "6",
                                                    },
                                                    {
                                                        "label": "Irregular, debris-covered",
                                                        "value": "7",
                                                    },
                                                    {
                                                        "label": "Single lobe, clean ice",
                                                        "value": "8",
                                                    },
                                                    {
                                                        "label": "Single lobe, debris-covered",
                                                        "value": "9",
                                                    },
                                                ],
                                                multi=True,
                                                value="None",
                                            ),
                                        ],
                                        className="selection_item",
                                    ),
                                ],
                            )
                        ],
                        className="mini_container selection_panel",
                    ),
                    md=4,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H5("Mass Balance", className="text-center",),
                            dcc.Graph(id="mass_balance"),
                        ],
                        className="mini_container ",
                    ),
                    md=4,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H5("Thickness Change", className="text-center",),
                            dcc.Graph(id="thickness_change"),
                        ],
                        className="mini_container ",
                    ),
                    md=4,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H5("Front Variation", className="text-center",),
                            dcc.Graph(id="front_variation"),
                        ],
                        className="mini_container ",
                    ),
                    md=4,
                ),
            ]
        ),
    ],
    fluid=True,
    className="main_container",
)

def ts_extend_helper(df):
    '''Extend timeseries of length one with a zero measurement in 2020 for plotting purposes'''
    df_out = df
    
    if df.shape[0] == 1:
        zero_frame = pd.DataFrame([[2020, 0]], columns=df.columns)
        df_out = df.append(zero_frame)
        
    return df_out

@app.callback(
    Output(component_id="glacier_info", component_property="children"),
    [Input(component_id="mapbox", component_property="clickData")],
)
def update_glacier_info_div(input_value):
    wgms_id = "N/A"
    if input_value:
        point_data = input_value["points"][0]
        wgms_id = point_data["customdata"]

    return f"{wgms_id}"


@app.callback(
    [
        Output(component_id="thickness_change", component_property="figure"),
        Output(component_id="mass_balance", component_property="figure"),
        Output(component_id="front_variation", component_property="figure"),
    ],
    [Input(component_id="mapbox", component_property="clickData")],
)
def update_glacier_figures(satellite_clickdata):

    if satellite_clickdata is None:
        satellite_clickdata = {"points": [{"customdata": mer_de_glace}]}

    selected = satellite_clickdata["points"][0]["customdata"]

    df_t = df_thickness.query("WGMS_ID == @selected").drop("WGMS_ID", axis=1)
    df_mb = df_massbalance.query("WGMS_ID == @selected").drop("WGMS_ID", axis=1)
    df_fv = df_front.query("WGMS_ID == @selected").drop("WGMS_ID", axis=1)
    
    df_t = ts_extend_helper(df_t)
    df_mb = ts_extend_helper(df_mb)
    df_fv = ts_extend_helper(df_fv)

    thickness_fig = dict(
        data=[dict(type="bar", x=df_t.YEAR, y=df_t.THICKNESS_CHG, width=1)],
        layout=dict(
            xaxis_title="Year",
            yaxis_title="(mm)",
            autosize=True,
            height=200,
            margin=dict(l=20, r=20, b=20, t=20, pad=0),
        ),
    )

    massbalance_fig = dict(
        data=[dict(type="bar", x=df_mb.YEAR, y=df_mb.ANNUAL_BALANCE, width=1)],
        layout=dict(
            xaxis_title="Year",
            yaxis_title="(mm w.e.)",
            autosize=True,
            height=200,
            margin=dict(l=20, r=20, b=20, t=20, pad=0),
        ),
    )
    frontvar_fig = dict(
        data=[dict(type="bar", x=df_fv.YEAR, y=df_fv.FRONT_VARIATION, width=1)],
        layout=dict(
            xaxis_title="Year",
            yaxis_title="(mm w.e.)",
            autosize=True,
            height=200,
            margin=dict(l=20, r=20, b=20, t=20, pad=0),
        ),
    )

    return thickness_fig, massbalance_fig, frontvar_fig


app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter
