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
from bar_charts import create_bar_charts
from line_charts import create_line_charts
from boxplot_charts import create_box_plots_figure
from bar_with_lines_chart import  create_bar_with_lines_chart
from pathlib import Path

# CLASS_ACTIVITY = "/class-activityy"
CLASS_ACTIVITY = "/class"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "LiDAR Data Visualization Dashboard"


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()
  return f"data:image/png;base64,{encoded}"


# -------------------------------
# Load data
# -------------------------------
def load_data(path):
  list_data = [
    'ecal_timestamp', 'object_id', 'confidence', 'nb_point',
    'algo_center_x', 'algo_center_y', 'algo_center_z'
  ]
  df = pd.read_csv(path)[list_data].copy()

  df['datetime'] = pd.to_datetime(df['ecal_timestamp'], unit='us', utc=True)

  df['time_in_seconds'] = (df['datetime'].dt.hour * 3600 +
                           df['datetime'].dt.minute * 60 +
                           df['datetime'].dt.second +
                           df['datetime'].dt.microsecond / 1_000_000)

  df['timestamp'] = df['time_in_seconds'].astype(int)

  df = df.drop(['time_in_seconds', 'datetime', 'ecal_timestamp'], axis=1)
  df = df.drop_duplicates(subset=['timestamp', 'object_id'], keep='first')

  first_60_unique_timestamps = df['timestamp'].unique()[:60]
  df = df[df['timestamp'].isin(first_60_unique_timestamps)]

  # filtered_df = df.query('object_id == 3')
  # filtered_df.to_csv(r'C:\Users\Axeel\iCloudDrive\Master_MCS\1st_Semester\Probabilidad_y_Estadistica\Presentacion_1\src\team_profe.csv')

  # Team 1    -> object 0
  # Team 2    -> object 2
  # Professor -> object 3

  return df


df = load_data(r"./algo_one_rec.csv")

# -------------------------------
# Navigation Layout
# -------------------------------
navbar = dbc.NavbarSimple(
  children=[
    dbc.NavItem(dbc.NavLink("Bar Charts", href="/bar-charts")),
    dbc.NavItem(dbc.NavLink("Line Charts", href="/line-charts")),
    dbc.NavItem(dbc.NavLink("Box Plots", href="/box-plots")),
    dbc.NavItem(dbc.NavLink("Class Activity", href=CLASS_ACTIVITY)),
    dbc.NavItem(dbc.NavLink("LiDAR Visualization", href="https://dash.gallery/dash-lyft-explorer", target="_blank")),
  ],
  brand="LiDAR Data Dashboard",
  brand_href="/",
  color="primary",
  dark=True,
  sticky="top",
)

# -------------------------------
# Home Page
# -------------------------------
home_layout = html.Div([
  html.H1("Welcome to LiDAR Data Visualization for Probability and Statistics", className="text-center my-4"),

  html.Div([
    dbc.Card(
      dbc.CardBody([
        html.H3("📊 Bar Charts", className="card-title"),
        html.P("Interactive bar charts showing confidence and point counts by object ID"),
        dbc.Button("Go to Bar Charts", href="/bar-charts", color="primary"),
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
    dbc.Card(
      dbc.CardBody([
        html.H3("👨‍🏫 Class Activity", className="card-title"),
        html.P("Interactive activity for students to estimate LiDAR parameters"),
        dbc.Button("Go to Activity", href=CLASS_ACTIVITY, color="primary"),
      ]),
      className="m-3"
    ),
  ], style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap'}),
], className="container")

# -------------------------------
# Bar Charts Page
# -------------------------------
bar_charts_layout = html.Div([
  html.H1("Bar Charts Analysis", className="text-center my-4"),
  html.P("Interactive bar charts showing aggregated data by object ID ranges",
         className="text-center text-muted mb-4"),
  dcc.Graph(
    id='bar-charts-graph',
    figure=create_bar_charts(df),
    config={'displayModeBar': True}
  ),
  dbc.Button("← Back to Home", href="/", color="secondary", className="mt-3"),
], className="container")

# -------------------------------
# Line Charts Page
# -------------------------------
line_charts_layout = html.Div([
  html.H1("Line Charts Analysis", className="text-center my-4"),
  html.P("Time series analysis of confidence and point counts over time",
         className="text-center text-muted mb-4"),
  dcc.Graph(
    id='line-charts-graph',
    figure=create_line_charts(df),
    config={'displayModeBar': True}
  ),
  dbc.Button("← Back to Home", href="/", color="secondary", className="mt-3"),
], className="container")

# -------------------------------
# Box Plots Page
# -------------------------------
box_plots_layout = html.Div([
  html.H1("Box Plots Analysis", className="text-center my-4"),
  html.P("Distribution analysis of various metrics across different objects",
         className="text-center text-muted mb-4"),
  dcc.Graph(
    id='box-plots-graph',
    figure=create_box_plots_figure(df),
    config={'displayModeBar': True}
  ),
  dbc.Button("← Back to Home", href="/", color="secondary", className="mt-3"),
], className="container")

# -------------------------------
# Class Activity  (NUEVO: mosaico 2x2 + inputs 3x4 + gráfico bar/line)
# -------------------------------
BASE = Path(__file__).parent  # rutas robustas relativas a este archivo
encoded_images = [encode_image(str(BASE / f"{i}.png")) for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)]

class_activity_layout = html.Div([
  html.H1("👨‍🏫 Class Activity: LiDAR Parameter Estimation", className="text-center my-4"),
  html.P("Estimate the parameters based on the 4 LiDAR images",
         className="text-center text-muted mb-4"),

  # Student info (lo conservamos tal cual)
  dbc.Row([
    dbc.Col([
      dbc.Card([
        dbc.CardHeader("Student Information"),
        dbc.CardBody([
          dbc.InputGroup([
            dbc.InputGroupText("Full Name"),
            dbc.Input(id="student-name", type="text", placeholder="Enter your full name"),
          ], className="mb-3"),
          html.Div(id="name-validation", className="text-danger"),
        ])
      ])
    ], width=6)
  ], justify="center", className="mb-4"),

  # Mosaico 2x2 (1.png, 2.png, 3.png, 4.png)
  dbc.Row([
    dbc.Col([
      dbc.Card([
        dbc.CardHeader("Reference Images (1–4)"),
        dbc.CardBody([
          dbc.Tabs([
            # Tab Team 1
            dbc.Tab(
              dbc.Container([
                dbc.Row([
                  dbc.Col(html.Img(src=encoded_images[0], style={"width": "100%", "borderRadius": "8px"}), md=6),
                  dbc.Col(html.Img(src=encoded_images[1], style={"width": "100%", "borderRadius": "8px"}), md=6),
                ], className="mb-3"),
                dbc.Row([
                  dbc.Col(html.Img(src=encoded_images[2], style={"width": "100%", "borderRadius": "8px"}), md=6),
                  dbc.Col(html.Img(src=encoded_images[3], style={"width": "100%", "borderRadius": "8px"}), md=6),
                ]),
                dbc.Row([
                  dbc.Col([
                    html.Div([
                      dcc.Download(id="download-csv"),
                      dbc.Button(
                        "Download Team 1 CSV",
                        id={"type": "download-btn", "index": "team1"},
                        color="success",
                        className="mt-3"
                      ),
                    ], className="text-center")
                  ], width=12)
                ], className="mt-4"),
              ], fluid=True),
              label="Team 1",
              tab_id="tab-1"
            ),
            # Tab Team 2
            dbc.Tab(
              dbc.Container([
                dbc.Row([
                  dbc.Col(html.Img(src=encoded_images[4], style={"width": "100%", "borderRadius": "8px"}), md=6),
                  dbc.Col(html.Img(src=encoded_images[5], style={"width": "100%", "borderRadius": "8px"}), md=6),
                ], className="mb-3"),
                dbc.Row([
                  dbc.Col(html.Img(src=encoded_images[6], style={"width": "100%", "borderRadius": "8px"}), md=6),
                  dbc.Col(html.Img(src=encoded_images[7], style={"width": "100%", "borderRadius": "8px"}), md=6),
                ]),
                dbc.Row([
                  dbc.Col([
                    html.Div([
                      dcc.Download(id="download-csv"),
                      dbc.Button(
                        "Download Team 2 CSV",
                        id={"type": "download-btn", "index": "team2"},
                        color="success",
                        className="mt-3"
                      ),
                    ], className="text-center")
                  ], width=12)
                ], className="mt-4"),
              ], fluid=True),
              label="Team 2",
              tab_id="tab-2"
            ),
            # Tab Professor
            dbc.Tab(
              dbc.Container([
                dbc.Row([
                  dbc.Col(html.Img(src=encoded_images[8], style={"width": "100%", "borderRadius": "8px"}), md=6),
                  dbc.Col(html.Img(src=encoded_images[9], style={"width": "100%", "borderRadius": "8px"}), md=6),
                ], className="mb-3"),
                dbc.Row([
                  dbc.Col(html.Img(src=encoded_images[10], style={"width": "100%", "borderRadius": "8px"}), md=6),
                  dbc.Col(html.Img(src=encoded_images[11], style={"width": "100%", "borderRadius": "8px"}), md=6),
                ]),
                dbc.Row([
                  dbc.Col([
                    html.Div([
                      dcc.Download(id="download-csv"),
                      dbc.Button(
                        "Download Professor's CSV",
                        id={"type": "download-btn", "index": "team3"},
                        color="success",
                        className="mt-3"
                      ),
                    ], className="text-center")
                  ], width=12)
                ], className="mt-4"),
              ], fluid=True),
              label="Professor",
              tab_id="tab-3"
            ),
          ]),
        ])
      ])
    ], width=10)
  ], justify="center", className="mb-4"),



  # Load CSV and show it in a table
  dbc.Row([
    dbc.Col([
      dbc.Card([
        dbc.CardHeader("Load and Display CSV Data"),
        dbc.CardBody([

          # File upload component
          dcc.Upload(
            id='upload-csv',
            children=html.Div([
              'Drag and Drop or ',
              html.A('Select Your CSV File')
            ]),
            style={
              'width': '100%',
              'height': '60px',
              'lineHeight': '60px',
              'borderWidth': '1px',
              'borderStyle': 'dashed',
              'borderRadius': '5px',
              'textAlign': 'center',
              'margin': '10px'
            },
            multiple=False
          ),

          dcc.Loading(
            id="loading-csv",
            type="circle",
            children=[html.Div(id="csv-table-container")]
          )
        ])
      ])
    ], width=10)
  ], justify="center", className="mb-4"),







  # Inputs 3 campos × 4 imágenes (conservamos los NOMBRES visibles de tu UI)
  # Fila de encabezados: Parámetro | Img1 | Img2 | Img3 | Img4
  # dbc.Row([
  #   dbc.Col([
  #     dbc.Card([
  #       dbc.CardHeader("Parameter Estimation (per image)"),
  #       dbc.CardBody([
  #         html.Table([
  #           html.Thead(
  #             html.Tr([
  #               html.Th("Parameter"),
  #               html.Th("Image 1"), html.Th("Image 2"),
  #               html.Th("Image 3"), html.Th("Image 4"),
  #             ])
  #           ),
  #           html.Tbody([
  #             # 1) Confidence
  #             html.Tr([
  #               html.Td("Confidence"),
  #               html.Td(dcc.Input(id="input-confidence-1", type="number")),
  #               html.Td(dcc.Input(id="input-confidence-2", type="number")),
  #               html.Td(dcc.Input(id="input-confidence-3", type="number")),
  #               html.Td(dcc.Input(id="input-confidence-4", type="number")),
  #             ]),
  #             # 2) Number of points
  #             html.Tr([
  #               html.Td("Number of points"),
  #               html.Td(dcc.Input(id="input-nbpoints-1", type="number")),
  #               html.Td(dcc.Input(id="input-nbpoints-2", type="number")),
  #               html.Td(dcc.Input(id="input-nbpoints-3", type="number")),
  #               html.Td(dcc.Input(id="input-nbpoints-4", type="number")),
  #             ]),
  #             # 3) Distance
  #             html.Tr([
  #               html.Td("Distance"),
  #               html.Td(dcc.Input(id="input-distance-1", type="number")),
  #               html.Td(dcc.Input(id="input-distance-2", type="number")),
  #               html.Td(dcc.Input(id="input-distance-3", type="number")),
  #               html.Td(dcc.Input(id="input-distance-4", type="number")),
  #             ]),
  #           ])
  #         ], className="table table-bordered")
  #       ])
  #     ])
  #   ], width=10)
  # ], justify="center", className="mb-4"),

  # Controles de gráfica
  # dbc.Row([
  #   dbc.Col([
  #     html.Label("Chart type"),
  #     dcc.Dropdown(
  #       id="activity-chart-type",
  #       options=[{"label": "Bar", "value": "bar"},
  #                {"label": "Line", "value": "line"}],
  #       value="bar",
  #       clearable=False
  #     )
  #   ], md=3),
  #   dbc.Col([
  #     html.Button("Update chart", id="activity-update", n_clicks=0,
  #                 style={"padding": "8px 14px", "fontWeight": 600})
  #   ], md=3),
  # ], className="mb-3", justify="start"),
  #
  # # Gráfico final
  # dcc.Graph(id="activity-xy-graph", figure=go.Figure()),


  dbc.Button("← Back to Home", href="/", color="secondary", className="mt-3"),
], className="container")


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
  if pathname == '/bar-charts':
    return bar_charts_layout
  elif pathname == '/line-charts':
    return line_charts_layout
  elif pathname == '/box-plots':
    return box_plots_layout
  elif pathname == CLASS_ACTIVITY:
    # return box_plots_layout
    return class_activity_layout
  else:
    return home_layout


# Download CSV
@app.callback(
  Output("download-csv", "data"),
  Input({"type": "download-btn", "index": ALL}, "n_clicks"),
  prevent_initial_call=True
)
def handle_downloads(btn_clicks):
  ctx = dash.callback_context
  if not ctx.triggered:
    return dash.no_update

  # Get which button was clicked
  triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
  triggered_id = eval(triggered_id)  # Convert string to dictionary
  team_name = triggered_id['index']

  # Map team names to CSV files
  csv_files = {
    "team1": "team_1.csv",
    "team2": "team_2.csv",
    "team3": "team_3.csv"
  }

  csv_filename = csv_files.get(team_name)
  if not csv_filename:
    return dict(content="Error: Team not found", filename="error.txt")

  csv_path = os.path.join('./', csv_filename)

  # Check if file exists
  if not os.path.exists(csv_path):
    return dict(content=f"Error: File {csv_filename} not found", filename="error.txt")

  # Read and return the CSV file
  with open(csv_path, 'r') as f:
    csv_content = f.read()

  return dict(content=csv_content, filename=f"{team_name}_data.csv")


# Load CSV
@app.callback(
    Output("csv-table-container", "children"),
    Input("upload-csv", "contents"),
    State("upload-csv", "filename"),
    prevent_initial_call=True
)
def load_and_display_csv(contents, filename):
  try:
    if contents is None:
      return html.Div("Please upload a CSV file")

    # Decode and read CSV
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

    # Create table
    table = dash_table.DataTable(
      data=df.to_dict("records"),
      columns=[{"name": col, "id": col} for col in df.columns],
      page_size=10,
      sort_action="native",
      filter_action="native",
      style_table={"overflowX": "auto"},
      style_cell={
        "textAlign": "left",
        "padding": "10px",
        "fontFamily": "Arial",
        "border": "1px solid #dee2e6"
      },
      style_header={
        "backgroundColor": "#f8f9fa",
        "fontWeight": "bold",
        "border": "2px solid #dee2e6"
      },
      style_data_conditional=[
        {
          "if": {"row_index": "odd"},
          "backgroundColor": "#f2f2f2"
        }
      ]
    )

    # Create chart
    fig = create_bar_with_lines_chart(df)
    chart = dcc.Graph(figure=fig, style={"marginTop": "20px"})

    # Return both table and chart
    return html.Div([
      html.H5(f"📂 Loaded file: {filename} ({df.shape[0]} rows, {df.shape[1]} columns)"),
      table,
      chart
    ])

  except Exception as e:
    return dbc.Alert(
      f"Error loading CSV: {str(e)}",
      color="danger",
      className="mt-3"
    )


# =========================
# @app.callback(
#   Output("csv-table-container", "children"),
#   Input("upload-csv", "contents"),
#   State("upload-csv", "filename"),
#   prevent_initial_call=True
# )
# def load_and_display_csv(contents, filename):
#   try:
#     if contents is None:
#       return html.Div("Please upload a CSV file")
#
#     # read CSV
#     content_type, content_string = contents.split(",")
#     decoded = base64.b64decode(content_string)
#     df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
#
#     # DataTable
#     return dash_table.DataTable(
#       data=df.to_dict("records"),
#       columns=[{"name": col, "id": col} for col in df.columns],
#       page_size=10,
#       sort_action="native",
#       filter_action="native",
#       style_table={"overflowX": "auto"},
#       style_cell={
#         "textAlign": "left",
#         "padding": "10px",
#         "fontFamily": "Arial",
#         "border": "1px solid #dee2e6"
#       },
#       style_header={
#         "backgroundColor": "#f8f9fa",
#         "fontWeight": "bold",
#         "border": "2px solid #dee2e6"
#       },
#       style_data_conditional=[
#         {
#           "if": {"row_index": "odd"},
#           "backgroundColor": "#f2f2f2"
#         }
#       ]
#     )
#
#   except Exception as e:
#     return dbc.Alert(
#       f"Error loading CSV: {str(e)}",
#       color="danger",
#       className="mt-3"
#     )




# -------------------------------
# Callbacks for Class Activity - UPDATED
# -------------------------------
def _num_or_none(x):
  if x is None: return None
  try: return float(str(x).strip())
  except: return None

@app.callback(
  Output("activity-xy-graph", "figure"),
  Input("activity-update", "n_clicks"),
  State("activity-chart-type", "value"),
  # Confidence x4
  State("input-confidence-1", "value"), State("input-confidence-2", "value"),
  State("input-confidence-3", "value"), State("input-confidence-4", "value"),
  # Number of points x4
  State("input-nbpoints-1", "value"), State("input-nbpoints-2", "value"),
  State("input-nbpoints-3", "value"), State("input-nbpoints-4", "value"),
  # Distance x4
  State("input-distance-1", "value"), State("input-distance-2", "value"),
  State("input-distance-3", "value"), State("input-distance-4", "value"),
)
def build_activity_chart(_n, chart_type,
                         c1, c2, c3, c4,
                         p1, p2, p3, p4,
                         d1, d2, d3, d4):
  x_labels = ["Img1", "Img2", "Img3", "Img4"]

  confidence = list(map(_num_or_none, [c1, c2, c3, c4]))
  nb_points  = list(map(_num_or_none, [p1, p2, p3, p4]))
  distance   = list(map(_num_or_none, [d1, d2, d3, d4]))

  series = [
    ("Confidence", confidence, "#1f77b4"),
    ("Number of points", nb_points, "#ff7f0e"),
    ("Distance", distance, "#2ca02c"),
  ]

  fig = go.Figure()
  any_data = False

  for name, yvals, color in series:
    if all(v is None for v in yvals):
      continue
    any_data = True
    y = [v if v is not None else None for v in yvals]

    if chart_type == "bar":
      fig.add_trace(go.Bar(
        x=x_labels, y=y, name=name, marker_color=color,
        hovertemplate="Image=%{x}<br>" + name + "=%{y}<extra></extra>"
      ))
    else:
      fig.add_trace(go.Scatter(
        x=x_labels, y=y, name=name, mode="lines+markers",
        line=dict(width=2, color=color), marker=dict(size=6),
        hovertemplate="Image=%{x}<br>" + name + "=%{y}<extra></extra>"
      ))

  if not any_data:
    fig.add_annotation(text="Enter values in at least one row.",
                       xref="paper", yref="paper", x=0.5, y=0.5,
                       showarrow=False, font=dict(size=14, color="#555"))

  fig.update_layout(
    title="Per-image chart (Confidence / Number of points / Distance)",
    xaxis_title="Image",
    yaxis_title="Value",
    barmode="group" if chart_type == "bar" else None,
    template="plotly_white",
    legend_title="Parameter",
    margin=dict(l=40, r=20, t=60, b=40),
    hovermode="x unified" if chart_type == "line" else "closest"
  )
  return fig


# -------------------------------
# Run the app
# -------------------------------
if __name__ == '__main__':
  app.run(debug=False, port=8050)