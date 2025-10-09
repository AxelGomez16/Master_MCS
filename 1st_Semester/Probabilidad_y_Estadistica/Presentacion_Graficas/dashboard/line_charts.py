import dash
from dash import dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_line_charts(df):
  fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=("Confidence", "Number of Points"),
    vertical_spacing=0.15
  )

  objects_ids = sorted(df["object_id"].unique())

  for obj in objects_ids:
    sub = df[df["object_id"] == obj]

    fig.add_trace(go.Scatter(
      x=sub["timestamp"],
      y=sub["confidence"],
      name=f"Object {obj}",
      mode="lines+markers",
      marker=dict(color='blue', size=6),
      customdata=sub[["object_id", "nb_point", "algo_center_x", "confidence"]],
      hovertemplate=(
        "Frame: %{x}<br>"
        "Nb points: %{customdata[1]}<br>"
        "Confidence: %{y}<br>"
        "Distance (m): %{customdata[2]:.2f}<extra></extra>"
      ),
      visible=(obj == 2)
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
      x=sub["timestamp"],
      y=sub["nb_point"],
      name=f"Object {obj}",
      mode="lines+markers",
      marker=dict(color='red', size=6),
      customdata=sub[["object_id", "nb_point", "algo_center_x", "confidence"]],
      hovertemplate=(
        "Frame: %{x}<br>"
        "Nb points: %{y}<br>"
        "Confidence: %{customdata[3]:.2f}<br>"
        "Distance (m): %{customdata[2]:.2f}<extra></extra>"
      ),
      visible=(obj == 2)
    ), row=2, col=1)

  buttons = []
  for obj in objects_ids:
    visibility = []
    for trace in fig.data:
      if trace.name == f"Object {obj}":
        visibility.append(True)
      else:
        visibility.append(False)

    buttons.append(dict(
      label=f"Object {obj}",
      method="update",
      args=[{"visible": visibility},
            {"title": {"text": f"Object {obj} - Confidence and Points"}}]
    ))

  fig.update_layout(
    updatemenus=[dict(
      active=objects_ids.index(2) if 2 in objects_ids else 0,
      buttons=buttons,
      x=1.1, y=1.15
    )],
    title=f"Object 2 - Confidence and Points" if 2 in objects_ids else "Confidence and Points",
    height=800
  )

  fig.update_xaxes(title_text="Timestamp", row=1, col=1)
  fig.update_xaxes(title_text="Timestamp", row=2, col=1)
  fig.update_yaxes(title_text="Confidence", row=1, col=1)
  fig.update_yaxes(title_text="Number of Points", row=2, col=1)

  return fig