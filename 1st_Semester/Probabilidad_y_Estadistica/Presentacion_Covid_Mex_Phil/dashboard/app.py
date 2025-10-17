import dash
from dash import dcc, html, Input, Output, callback_context, State, ALL, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import os
import io
import csv
from datetime import datetime
from weekly_cases import *

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Mexico vs Philippines Data Visualization Dashboard"



# -------------------------------
# Navigation Layout
# -------------------------------
navbar = dbc.NavbarSimple(
  children=[
    # dbc.NavItem(dbc.NavLink("Weekly cases - Map world", href="/bar-charts")),
    dbc.NavItem(dbc.NavLink("Weekly cases", href="/weekly-cases")),
    # dbc.NavItem(dbc.NavLink("Line Charts", href="/line-charts")),
    # dbc.NavItem(dbc.NavLink("Box Plots", href="/box-plots")),
    # dbc.NavItem(dbc.NavLink("LiDAR Visualization", href="https://dash.gallery/dash-lyft-explorer", target="_blank")),
  ],
  brand="COVID 19 Data Dashboard: Mexico vs Philippines",
  brand_href="/",
  color="primary",
  dark=True,
  sticky="top",
)

# -------------------------------
# Home Page
# -------------------------------
home_layout = html.Div([
  html.H1("Welcome to COVID 19 Data Visualization for Mexico vs Philippines", className="text-center my-4"),

  html.Div([
    dbc.Card(
      dbc.CardBody([
        html.H3("📊 Weekly cases", className="card-title"),
        html.P("Interactive map showing weekly cases by country"),
        dbc.Button("Go to weekly cases", href="/weekly-cases", color="primary"),
      ]),
      className="m-3"
    ),
    dbc.Card(
      dbc.CardBody([
        html.H3("📈 Line Charts", className="card-title"),
        html.P("Time series line charts showing confidence and point trends"),
        dbc.Button("Go to Line Charts", href="/line-charts", color="primary"),
      ]),
      className="m-3"
    ),
    dbc.Card(
      dbc.CardBody([
        html.H3("📦 Box Plots", className="card-title"),
        html.P("Distribution analysis using box plots for various metrics"),
        dbc.Button("Go to Box Plots", href="/box-plots", color="primary"),
      ]),
      className="m-3"
    ),
    dbc.Card(
      dbc.CardBody([
        html.H3("🌨️ LiDAR Visualization", className="card-title"),
        html.P("Interactive data visualization for point cloud on the street"),
        dbc.Button("Go to LiDAR Visualization", href="https://dash.gallery/dash-lyft-explorer", color="primary",
                   target="_blank"),
      ]),
      className="m-3"
    ),
  ], style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap'}),
], className="container")




# -------------------------------
# Map Page
# -------------------------------
choropleth_layout = weekly_cases_layout()


# -------------------------------
# App Layout and Routing
# -------------------------------
app.layout = html.Div([
  dcc.Location(id='url', refresh=False),
  navbar,
  html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
  if pathname == '/weekly-cases':
    return choropleth_layout
  # elif pathname == '/line-charts':
  #   return line_charts_layout
  # elif pathname == '/box-plots':
  #   return box_plots_layout
  else:
    return home_layout



# -------------------------------
# Run the app
# -------------------------------
if __name__ == '__main__':
  app.run(debug=True, port=8050)