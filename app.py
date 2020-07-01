import plotly.graph_objects as go
import pandas as pd
import numpy as np
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
                                            [html.H3(id="num_glaciers"), "Glaciers"],
                                            className="mini_container",
                                        ),
                                    ],
                                    width=3,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [html.H3(id="num_data_points"), "Data Points"],
                                        className="mini_container",
                                    ),
                                    width=3,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.H3(id="earliest_record"),
                                            "Oldest Record",
                                        ],
                                        className="mini_container",
                                    ),
                                    width=3,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [html.H3(id="num_countries"), "Countries"],
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
                                        dcc.Graph(id="mapbox"),
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
                                                id="first_measurement_slider",
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
                                                id="years_data_slider",
                                                min=0,
                                                max=20,
                                                step=1,
                                                value=0,
                                                marks={
                                                    0: "0+",
                                                    4: "4+",
                                                    8: "8+",
                                                    12: "12+",
                                                    16: "16+",
                                                    20: "20+",
                                                },
                                            ),
                                        ],
                                        className="selection_item",
                                    ),
                                    html.Div(
                                        [
                                            html.P("Filter by Primary Classification:"),
                                            dcc.Dropdown(
                                                id="prim_classific_dropdown",
                                                options=[
                                                    {
                                                        "label": "Miscellaneous",
                                                        "value": 0,
                                                    },
                                                    {
                                                        "label": "Continental ice sheet",
                                                        "value": 1,
                                                    },
                                                    {"label": "Ice Field", "value": 2,},
                                                    {"label": "Ice Cap", "value": 3},
                                                    {
                                                        "label": "Outlet Glacier",
                                                        "value": 4,
                                                    },
                                                    {
                                                        "label": "Valley Glacier",
                                                        "value": 5,
                                                    },
                                                    {
                                                        "label": "Mountain glacier ",
                                                        "value": 6,
                                                    },
                                                    {
                                                        "label": "Glacieret and snowfield",
                                                        "value": 7,
                                                    },
                                                    {"label": "Ice Shelf", "value": 8,},
                                                    {
                                                        "label": "Rock Glacier",
                                                        "value": 9,
                                                    },
                                                    {"label": "Unknown", "value": 10,},
                                                ],
                                                multi=True,
                                                value=None,
                                            ),
                                        ],
                                        className="selection_item",
                                    ),
                                    html.Div(
                                        [
                                            html.P("Filter by Form:"),
                                            dcc.Dropdown(
                                                id="form_dropdown",
                                                options=[
                                                    {
                                                        "label": "Miscellaneous",
                                                        "value": 0,
                                                    },
                                                    {
                                                        "label": "Compound Basins",
                                                        "value": 1,
                                                    },
                                                    {
                                                        "label": "Compound Basin",
                                                        "value": 2,
                                                    },
                                                    {
                                                        "label": "Simple Basin",
                                                        "value": 3,
                                                    },
                                                    {"label": "Circque", "value": 4},
                                                    {"label": "Niche", "value": 5},
                                                    {"label": "Crater", "value": 6},
                                                    {"label": "Ice Apron", "value": 7,},
                                                    {"label": "Group", "value": 8},
                                                    {"label": "Remnant", "value": 9},
                                                    {"label": "Unknown", "value": 10},
                                                ],
                                                multi=True,
                                                value=[],
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
                                                id="frontal_chars_dropdown",
                                                options=[
                                                    {
                                                        "label": "Miscellaneous",
                                                        "value": 0,
                                                    },
                                                    {"label": "Piedmont", "value": 1,},
                                                    {
                                                        "label": "Expanded Foot",
                                                        "value": 2,
                                                    },
                                                    {"label": "Lobed", "value": 3},
                                                    {"label": "Calving", "value": 4},
                                                    {
                                                        "label": "Coalescing, non-contributing",
                                                        "value": 5,
                                                    },
                                                    {
                                                        "label": "Irregular, clean ice",
                                                        "value": 6,
                                                    },
                                                    {
                                                        "label": "Irregular, debris-covered",
                                                        "value": 7,
                                                    },
                                                    {
                                                        "label": "Single lobe, clean ice",
                                                        "value": 8,
                                                    },
                                                    {
                                                        "label": "Single lobe, debris-covered",
                                                        "value": 9,
                                                    },
                                                    {"label": "Unknown", "value": 10},
                                                ],
                                                multi=True,
                                                value=[],
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
                            html.H5("Detailed Information", className="text-center",),
                            html.Table(
                                html.Tbody(
                                    [
                                        html.Tr(
                                            [
                                                html.Td(id="info_name"),
                                                html.Td(id="info_wgms_id"),
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td(id="info_geography"),
                                                html.Td(id="info_political_unit"),
                                            ]
                                        ),
                                        html.Tr(
                                            [
                                                html.Td(id="info_elevation"),
                                                html.Td(id="info_lat_long"),
                                            ]
                                        ),
                                        html.Tr(
                                            [html.Td(id="info_reference", colSpan=2,),]
                                        ),
                                        html.Tr(
                                            [html.Td(id="info_sponsor", colSpan=2,),]
                                        ),
                                        html.Tr(
                                            [html.Td(id="info_remarks", colSpan=2,),]
                                        ),
                                    ]
                                ),
                                className="glacier_info_item",
                            ),
                        ],
                        className="mini_container glacier_info_panel ",
                    ),
                    md=4,
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H5("Mass Balance", className="text-center",),
                                dcc.Graph(id="mass_balance"),
                            ],
                            className="mini_container ",
                        ),
                        html.Div(
                            [
                                html.H5("Thickness Change", className="text-center",),
                                dcc.Graph(id="thickness_change"),
                            ],
                            className="mini_container ",
                        ),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H5("Front Variation", className="text-center",),
                                dcc.Graph(id="front_variation"),
                            ],
                            className="mini_container ",
                        ),
                    ],
                    md=4,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H5("Error messages", className="text-center",),
                            html.Div(id="error-div"),
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
    """Extend timeseries of length one with a zero measurement in 2020 for plotting purposes"""

    df_out = df

    if df.shape[0] == 1:
        zero_frame = pd.DataFrame([[2020, 0]], columns=df.columns)
        df_out = df.append(zero_frame)

    return df_out


def glacier_filter_helper(
    df, first_meas, years_data, prim_classific, form, frontal_chars
):
    """Apply glacier selection filters to dataframe"""

    # Default is to display all data
    dropdown_all = list(range(11))
    if not prim_classific:
        prim_classific = dropdown_all
    if not form:
        form = dropdown_all
    if not frontal_chars:
        frontal_chars = dropdown_all

    # Apply Filters
    dff = (
        df.query("FIRST_MEAS < @first_meas")
        .query("YEAR_MEASUREMENTS > @years_data")
        .query("PRIM_CLASSIFIC in @prim_classific")
        .query("FORM in @form")
        .query("FRONTAL_CHARS in @frontal_chars")
    )

    return dff


def num_data_points_helper(unique_ids):
    """Determine total number of datapoints in thickness, mass balance, and front variation datasets for a set of wgms id's"""

    dfs = [df_thickness, df_massbalance, df_front]
    num_data_points = sum(
        [df[df["WGMS_ID"].isin(unique_ids)].iloc[:, 0].count() for df in dfs]
    )
    print(unique_ids)
    return num_data_points


# Satellite Map


@app.callback(
    [
        Output(component_id="mapbox", component_property="figure"),
        Output(component_id="error-div", component_property="children"),
        Output(component_id="num_glaciers", component_property="children"),
        Output(component_id="earliest_record", component_property="children"),
        Output(component_id="num_countries", component_property="children"),
        Output(component_id="num_data_points", component_property="children"),
    ],
    [
        Input(component_id="first_measurement_slider", component_property="value"),
        Input(component_id="years_data_slider", component_property="value"),
        Input(component_id="prim_classific_dropdown", component_property="value"),
        Input(component_id="form_dropdown", component_property="value"),
        Input(component_id="frontal_chars_dropdown", component_property="value"),
    ],
)
def update_satellite_map(first_meas, years_data, prim_classific, form, frontal_chars):
    """Update main satellite map and four info boxes above it based on selected filters """

    df = glacier_filter_helper(
        df_combined, first_meas, years_data, prim_classific, form, frontal_chars
    )

    num_glaciers = f"{len(df.index):,}"
    first_meas = df["FIRST_MEAS"].min()
    earliest_record = f"{first_meas:.0f}" if first_meas is not np.nan else f"N/A"
    num_countries = df["POLITICAL_UNIT"].nunique()
    unique_ids = df["WGMS_ID"].unique()
    num_data_points = f"{num_data_points_helper(unique_ids):,}"

    map_data = [
        dict(
            type="scattermapbox",
            lon=df["LONGITUDE"],
            lat=df["LATITUDE"],
            customdata=df["WGMS_ID"],
            mode="markers",
            marker=go.scattermapbox.Marker(size=8, opacity=0.3),
        )
    ]

    layout = dict(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=0,
        mapbox_center_lon=0,
        mapbox_zoom=0,
        mapbox=dict(style="stamen-terrain", zoom=0, center=dict(lat=0, lon=0)),
        autosize=True,
        height=300,
        margin=dict(l=0, r=0, b=0, t=0, pad=50),
        legend=dict(font=dict(size=10), orientation="h"),
    )
    satellite_map = dict(data=map_data, layout=layout)

    return (
        satellite_map,
        str(unique_ids),
        num_glaciers,
        earliest_record,
        num_countries,
        num_data_points,
    )


@app.callback(
    [
        Output(component_id="info_name", component_property="children"),
        Output(component_id="info_wgms_id", component_property="children"),
        Output(component_id="info_geography", component_property="children"),
        Output(component_id="info_political_unit", component_property="children"),
        Output(component_id="info_elevation", component_property="children"),
        Output(component_id="info_lat_long", component_property="children"),
        Output(component_id="info_reference", component_property="children"),
        Output(component_id="info_sponsor", component_property="children"),
        Output(component_id="info_remarks", component_property="children"),
    ],
    [Input(component_id="mapbox", component_property="clickData")],
)
def update_glacier_info_div(input_value):
    """Update Detailed Information Panel based on satellite map clickdata"""
    wgms_id = mer_de_glace
    outputs = []

    if input_value:
        point_data = input_value["points"][0]
        wgms_id = point_data["customdata"]

    df = df_combined[df_combined["WGMS_ID"] == wgms_id].reset_index()
    text_keys = dict(
        NAME="Name:",
        WGMS_ID="WGMS Id:",
        SPEC_LOCATION="Geographic Location:",
        POLITICAL_UNIT="Country/Territory:",
        ELEVATION="Elevation Range (m):",
        LAT_LONG="Lat - Long:",
        REFERENCE="Reference:",
        SPONS_AGENCY="Sponsoring Agency:",
        REMARKS="Remarks:",
    )

    for key, text in text_keys.items():

        if key not in ["ELEVATION", "LAT_LONG"]:
            value = df.at[0, key]
        elif key == "ELEVATION":
            he = df.at[0, "HIGHEST_ELEVATION"]
            le = df.at[0, "LOWEST_ELEVATION"]

            highest_elev = f"{he:.0f}" if not np.isnan(he) else "N/A"
            lowest_elev = f"{le:.0f}" if not np.isnan(le) else "N/A"

            value = f"{lowest_elev} to {highest_elev}"

        elif key == "LAT_LONG":
            value = f"{df.at[0,'LATITUDE']:.2f}, {df.at[0,'LONGITUDE']:.2f}"

        # Special considerations for Elevation, Lat/Long, and Reference
        if key == "REFERENCE":
            if len(value) > 100:
                value = value[0:100] + "..."

        outputs.append([text, html.Br(), value])

    return outputs


@app.callback(
    [
        Output(component_id="thickness_change", component_property="figure"),
        Output(component_id="mass_balance", component_property="figure"),
        Output(component_id="front_variation", component_property="figure"),
    ],
    [Input(component_id="mapbox", component_property="clickData")],
)
def update_glacier_figures(satellite_clickdata):
    """ Update time series figures of mass balance, length, area, and thickness change """

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
