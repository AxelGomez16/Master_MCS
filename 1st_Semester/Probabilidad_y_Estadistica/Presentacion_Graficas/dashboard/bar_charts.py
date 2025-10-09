import dash
from dash import dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_bar_charts(df):
  agg_df = df.groupby('object_id').agg({
    'confidence': 'mean',
    'nb_point': 'sum',
    'algo_center_x': 'mean'
  }).reset_index()

  fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=("Confidence", "Total Number of Points"),
    vertical_spacing=0.15
  )

  objects_ids = sorted(agg_df["object_id"].unique())

  colors = px.colors.qualitative.Plotly
  color_map = {}
  for i, obj in enumerate(objects_ids):
    color_map[obj] = colors[i % len(colors)]

  object_ranges = []
  for i in range(0, len(objects_ids), 10):
    object_ranges.append(objects_ids[i:i + 10])

  for obj in objects_ids:
    sub = agg_df[agg_df["object_id"] == obj]

    fig.add_trace(go.Bar(
      x=sub["object_id"],
      y=sub["confidence"],
      name=f"Object {obj}",
      marker_color=color_map[obj],
      customdata=sub[["object_id", "nb_point", "algo_center_x", "confidence"]],
      hovertemplate=(
        "Object: %{x}<br>"
        "Nb Points: %{customdata[1]}<br>"
        "Confidence: %{y:.2f}<br>"
        "Distance (m): %{customdata[2]:.2f}<extra></extra>"
      ),
      visible=False
    ), row=1, col=1)

    fig.add_trace(go.Bar(
      x=sub["object_id"],
      y=sub["nb_point"],
      name=f"Object {obj}",
      marker_color=color_map[obj],
      customdata=sub[["object_id", "nb_point", "algo_center_x", "confidence"]],
      hovertemplate=(
        "Object: %{x}<br>"
        "Nb Points: %{y}<br>"
        "Confidence: %{customdata[3]:.2f}<br>"
        "Distance (m): %{customdata[2]:.2f}<extra></extra>"
      ),
      visible=False
    ), row=2, col=1)

  buttons = []
  for i, obj_range in enumerate(object_ranges):
    visibility = []
    for trace in fig.data:
      obj_num = int(trace.name.split(" ")[1])
      visibility.append(obj_num in obj_range)

    buttons.append(dict(
      label=f"Objects {obj_range[0]}-{obj_range[-1]}",
      method="update",
      args=[{"visible": visibility},
            {"title": {"text": f"Objects {obj_range[0]}-{obj_range[-1]} - Confidence and Points"}}]
    ))

  initial_visibility = []
  for trace in fig.data:
    obj_num = int(trace.name.split(" ")[1])
    initial_visibility.append(obj_num in object_ranges[0])

  fig.update_layout(
    updatemenus=[dict(
      active=0,
      buttons=buttons,
      x=1.1, y=1.15
    )],
    title=f"Objects {object_ranges[0][0]}-{object_ranges[0][-1]} - Confidence and Points",
    height=800,
    showlegend=False
  )

  for i, trace in enumerate(fig.data):
    trace.visible = initial_visibility[i]

  fig.update_xaxes(title_text="Object ID", row=1, col=1)
  fig.update_xaxes(title_text="Object ID", row=2, col=1)
  fig.update_yaxes(title_text="Confidence", row=1, col=1)
  fig.update_yaxes(title_text="Number of Points", row=2, col=1)

  return fig