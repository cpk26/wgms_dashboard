from dash_html_components.Tr import Tr
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
df_length = pd.read_pickle("wgms_length")
df_area = pd.read_pickle("wgms_area")


# Default selection is Mer De Glace, WGMS_ID = 353
mer_de_glace = 353

# Dash App

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,],)

server = app.server

# Checkbox styling
cb_inputStyle = {"vertical-align": "middle", "margin": "auto"}
cb_labelStyle = {"vertical-align": "middle"}
cb_style = {
    "display": "inline-flex",
    "flex-wrap": "wrap",
    "justify-content": "space-between",
    "line-height": "28px",
}


# Layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            "World Glacier Monitoring Service",
                            className="header text-center",
                        ),
                        html.Div(
                            "Fluctuations of Glaciers Data Explorer",
                            className="sub-header text-center",
                        ),
                    ],
                    md=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.Div(
                                [
                                    "Dashboard by ",
                                    html.A(
                                        "Inlet Labs",
                                        href="https://inletlabs.com/",
                                        className="info_link",
                                    ),
                                    ". Based on WGMS ",
                                    html.A(
                                        "2019 Data",
                                        href="https://wgms.ch/data_databaseversions/",
                                        className="info_link",
                                    ),
                                    ".",
                                ],
                                className="bottom_info_container text-center offset-md-8",
                            ),
                        ],
                    ),
                    md=12,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Col(
                            [
                                # presumptive entry
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Div(
                                                    [
                                                        html.H3(id="num_glaciers"),
                                                        "Glaciers",
                                                    ],
                                                    className="mini_container",
                                                ),
                                            ],
                                            width=3,
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    html.H3(id="num_data_points"),
                                                    "Data Points",
                                                ],
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
                                                [
                                                    html.H3(id="num_countries"),
                                                    "Countries",
                                                ],
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
                                            className="satellite_container",
                                        ),
                                        width=12,
                                    ),
                                    className="flex-grow-1 mini_container",
                                ),
                            ],
                            className="h-100 d-flex flex-column",
                        ),
                        # presumptive exit
                    ],
                    className="container-fluid ",
                    md=8,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.P("Filter by Earliest Measurement:"),
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
                                            html.P("Filter by Years of Data:"),
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
                                                    {"label": "Cirque", "value": 4},
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
                                    html.Div(
                                        [
                                            html.P("Filter by Available Data:"),
                                            html.Table(
                                                [
                                                    html.Tr(
                                                        [
                                                            html.Td(
                                                                dcc.Checklist(
                                                                    id="checkbox_mb",
                                                                    options=[
                                                                        {
                                                                            "label": " Mass Balance",
                                                                            "value": 1,
                                                                        },
                                                                    ],
                                                                    inputStyle=cb_inputStyle,
                                                                    labelStyle=cb_labelStyle,
                                                                    style=cb_style,
                                                                ),
                                                            ),
                                                            html.Td(
                                                                dcc.Checklist(
                                                                    id="checkbox_length",
                                                                    options=[
                                                                        {
                                                                            "label": " Length",
                                                                            "value": 1,
                                                                        },
                                                                    ],
                                                                    inputStyle=cb_inputStyle,
                                                                    labelStyle=cb_labelStyle,
                                                                    style=cb_style,
                                                                )
                                                            ),
                                                        ],
                                                    ),
                                                    html.Tr(
                                                        [
                                                            html.Td(
                                                                dcc.Checklist(
                                                                    id="checkbox_tc",
                                                                    options=[
                                                                        {
                                                                            "label": " Thickness Change",
                                                                            "value": 1,
                                                                        },
                                                                    ],
                                                                    inputStyle=cb_inputStyle,
                                                                    labelStyle=cb_labelStyle,
                                                                    style=cb_style,
                                                                )
                                                            ),
                                                            html.Td(
                                                                dcc.Checklist(
                                                                    id="checkbox_area",
                                                                    options=[
                                                                        {
                                                                            "label": " Area",
                                                                            "value": 1,
                                                                        },
                                                                    ],
                                                                    inputStyle=cb_inputStyle,
                                                                    labelStyle=cb_labelStyle,
                                                                    style=cb_style,
                                                                )
                                                            ),
                                                        ],
                                                        className="checkbox_table",
                                                    ),
                                                ],
                                                className="ts_table checkbox_table",
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
                                html.H5(
                                    "Mass Balance [mm w.e]", className="text-center",
                                ),
                                dcc.Graph(id="mass_balance"),
                            ],
                            className="mini_container ",
                        ),
                        html.Div(
                            [
                                html.H5(
                                    "Thickness Change [mm]", className="text-center",
                                ),
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
                                html.H5("Length [km]", className="text-center",),
                                dcc.Graph(id="length_ts"),
                            ],
                            className="mini_container ",
                        ),
                        html.Div(
                            [
                                html.H5(["Area [1000 m²]"], className="text-center",),
                                dcc.Graph(id="area_ts"),
                            ],
                            className="mini_container ",
                        ),
                    ],
                    md=4,
                ),
            ]
        ),
    ],
    fluid=True,
    className="main_container",
)


no_data_fig = dict(
    layout=dict(
        xaxis={"visible": False},
        yaxis={"visible": False},
        autosize=True,
        height=200,
        margin=dict(l=40, r=20, b=20, t=20, pad=1),
        annotations=[
            dict(
                text="No Available Data",
                xref="paper",
                yref="paper",
                showarrow=False,
                font={"size": 14},
            )
        ],
    )
)


# Extend time series -- not used
def ts_extend_helper(df):
    """Extend timeseries of length one with a zero measurement in 2020 for plotting purposes"""

    df_out = df

    if df.shape[0] == 1:
        df_out.loc[len(df_out), :] = 0
        df_out.loc[len(df_out), "YEAR"] = 2020

    return df_out


def glacier_filter_helper(
    df,
    first_meas,
    years_data,
    prim_classific,
    form,
    frontal_chars,
    checkbox_mb,
    checkbox_length,
    checkbox_tc,
    checkbox_area,
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

    checkbox_mb = [True] if checkbox_mb == [1] else [True, False]
    checkbox_length = [True] if checkbox_length == [1] else [True, False]
    checkbox_tc = [True] if checkbox_tc == [1] else [True, False]
    checkbox_area = [True] if checkbox_area == [1] else [True, False]

    # Apply Filters
    dff = (
        df.query("FIRST_MEAS <= @first_meas")
        .query("YEAR_MEASUREMENTS >= @years_data")
        .query("PRIM_CLASSIFIC in @prim_classific")
        .query("FORM in @form")
        .query("FRONTAL_CHARS in @frontal_chars")
        .query("THICKNESS_CHANGE_TS in @checkbox_tc")
        .query("LENGTH_TS in @checkbox_length")
        .query("AREA_TS in @checkbox_area")
        .query("MASS_BALANCE_TS in @checkbox_mb")
    )

    return dff


def num_data_points_helper(unique_ids):
    """Determine total number of datapoints in thickness, mass balance, and length variation datasets for a set of wgms id's"""

    dfs = [df_thickness, df_massbalance, df_length, df_area]
    num_data_points = sum(
        [df[df["WGMS_ID"].isin(unique_ids)].iloc[:, 0].count() for df in dfs]
    )
    print(unique_ids)
    return num_data_points


# Satellite Map


@app.callback(
    [
        Output(component_id="mapbox", component_property="figure"),
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
        Input(component_id="checkbox_mb", component_property="value"),
        Input(component_id="checkbox_length", component_property="value"),
        Input(component_id="checkbox_tc", component_property="value"),
        Input(component_id="checkbox_area", component_property="value"),
    ],
)
def update_satellite_map(
    first_meas,
    years_data,
    prim_classific,
    form,
    frontal_chars,
    checkbox_mb,
    checkbox_length,
    checkbox_tc,
    checkbox_area,
):
    """Update main satellite map and four info boxes above it based on selected filters """

    df = glacier_filter_helper(
        df_combined,
        first_meas,
        years_data,
        prim_classific,
        form,
        frontal_chars,
        checkbox_mb,
        checkbox_length,
        checkbox_tc,
        checkbox_area,
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
            customdata=df.loc[:, ["NAME", "WGMS_ID"]].values,
            tname=df["NAME"].values,
            mode="markers",
            marker=go.scattermapbox.Marker(size=8, opacity=0.7),
            hovertemplate="<b>%{customdata[0]}</b><br>Lat: %{lat:.2f} <br>Lon: %{lon:.2f}<extra></extra>",
        )
    ]

    layout = dict(
        mapbox_style="stamen-terrain",
        mapbox_center_lat=0,
        mapbox_center_lon=0,
        mapbox_zoom=0,
        mapbox=dict(style="stamen-terrain", zoom=0, center=dict(lat=0, lon=0)),
        # autosize=True,
        height=425,
        margin=dict(l=0, r=0, b=0, t=0, pad=0),
        legend=dict(font=dict(size=10), orientation="h"),
    )
    satellite_map = dict(data=map_data, layout=layout)

    return (
        satellite_map,
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
        wgms_id = point_data["customdata"][1]

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

        outputs.append([html.B(text), html.Br(), value])

    return outputs


@app.callback(
    [
        Output(component_id="thickness_change", component_property="figure"),
        Output(component_id="mass_balance", component_property="figure"),
        Output(component_id="length_ts", component_property="figure"),
        Output(component_id="area_ts", component_property="figure"),
    ],
    [Input(component_id="mapbox", component_property="clickData")],
)
def update_glacier_figures(satellite_clickdata):
    """ Update time series figures of mass balance, length, area, and thickness change """

    if satellite_clickdata is None:
        satellite_clickdata = {
            "points": [{"customdata": ["Mer de Glace", mer_de_glace]}]
        }

    selected = satellite_clickdata["points"][0]["customdata"][1]

    df_t = df_thickness.query("WGMS_ID == @selected").drop("WGMS_ID", axis=1)
    df_mb = df_massbalance.query("WGMS_ID == @selected").drop("WGMS_ID", axis=1)
    df_l = df_length.query("WGMS_ID == @selected").drop("WGMS_ID", axis=1)
    df_a = df_area.query("WGMS_ID == @selected").drop("WGMS_ID", axis=1)

    # df_t = ts_extend_helper(df_t)
    # df_mb = ts_extend_helper(df_mb)
    # df_l = ts_extend_helper(df_l)
    # df_a = ts_extend_helper(df_a)

    thickness_fig = massbalance_fig = length_fig = area_fig = no_data_fig

    if not df_t.empty:
        traces = []

        for _, row in df_t.iterrows():
            x = [row["REFERENCE_DATE"], row["YEAR"]]
            y = [row["THICKNESS_CHG"], row["THICKNESS_CHG"]]
            trace = dict(type="scatter", x=x, y=y, width=1, showlegend=False)
            traces.append(trace)

        thickness_fig = dict(
            data=traces,
            layout=dict(
                autosize=True,
                height=200,
                margin=dict(l=45, r=20, b=20, t=20, pad=1),
                yaxis=dict(tickformat=".0f"),
            ),
        )

    if not df_mb.empty:
        massbalance_fig = dict(
            data=[
                dict(
                    type="bar",
                    x=df_mb.YEAR,
                    y=df_mb.ANNUAL_BALANCE,
                    width=1,
                    marker=dict(opacity=0.3,),
                )
            ],
            layout=dict(
                autosize=True,
                height=200,
                xaxis=dict(tickformat=".0f"),
                margin=dict(l=40, r=20, b=20, t=20, pad=1),
            ),
        )

    if not df_l.empty:
        length_fig = dict(
            data=[
                dict(
                    type="bar",
                    orientation="h",
                    y=df_l.YEAR,
                    x=df_l.LENGTH,
                    width=1,
                    marker=dict(size=12, opacity=0.3,),
                )
            ],
            layout=dict(
                mode="lines+markers",
                autosize=True,
                height=200,
                margin=dict(l=50, r=20, b=20, t=20, pad=1),
                yaxis=dict(tickformat=".0f"),
            ),
        )

    if not df_a.empty:
        area_fig = dict(
            data=[
                dict(
                    type="scatter",
                    x=df_a.YEAR,
                    y=df_a.AREA,
                    width=1,
                    fill="tonexty",
                    marker=dict(color="rgb(158,202,225)", opacity=1,),
                    line=dict(color="rgb(158,202,225)"),
                )
            ],
            layout=dict(
                autosize=True,
                height=200,
                margin=dict(l=40, r=20, b=20, t=20, pad=1),
                xaxis=dict(tickformat=".0f"),
            ),
        )

    return thickness_fig, massbalance_fig, length_fig, area_fig


if __name__ == "__main__":
    app.run_server(debug=True)
