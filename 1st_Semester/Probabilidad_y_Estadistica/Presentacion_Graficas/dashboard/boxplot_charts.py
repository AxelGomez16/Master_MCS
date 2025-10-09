import dash
from dash import dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Box Plots Page
# -------------------------------
def create_box_plots_figure(df):
    # Division por grupos de 30
    object_ids_all = sorted(df["object_id"].unique())
    object_id_groups = [object_ids_all[i:i + 30] for i in range(0, len(object_ids_all), 30)]
    if not object_id_groups:
        raise ValueError("No hay object_id disponibles para graficar.")

    traces = []
    y_nb_all = []
    y_conf_all = []

    for obj in object_ids_all:
        sub = df[df["object_id"] == obj]
        if sub.empty:
            continue

        y_nb = sub["nb_point"].tolist()
        y_cf = sub["confidence"].tolist()
        x_cat = [obj] * len(sub)

        y_nb_all.append(y_nb)
        y_conf_all.append(y_cf)

        traces.append(go.Box(
            y=y_nb,
            x=x_cat,
            name=f"Objeto {obj}",
            boxpoints="all",
            jitter=0.3,
            pointpos=-1.8,
            visible=False
        ))

    if not traces:
        raise ValueError("No hay datos válidos para construir los boxplots.")

    fig = go.Figure(data=traces)

    total_traces = len(fig.data)

    def visibility_mask_for_group(g_idx: int):
        visible_ids = set(object_id_groups[g_idx])
        mask = []
        for tr in fig.data:
            # Get the object ID from the trace name
            obj_id_str = tr.name.replace("Objeto ", "")
            try:
                obj_id = int(obj_id_str)
                mask.append(obj_id in visible_ids)
            except ValueError:
                mask.append(False)
        return mask

    initial_group = 0
    fig_visibility_init = visibility_mask_for_group(initial_group)
    for tr, vis in zip(fig.data, fig_visibility_init):
        tr.visible = vis

    metric_buttons = [
        dict(
            label="nb_point",
            method="restyle",
            args=[{"y": y_nb_all}, list(range(total_traces))]
        ),
        dict(
            label="confidence",
            method="restyle",
            args=[{"y": y_conf_all}, list(range(total_traces))]
        )
    ]

    group_buttons = []
    for g_idx, group in enumerate(object_id_groups):
        vis = visibility_mask_for_group(g_idx)
        label = f"Grupo {g_idx+1} ({group[0]} - {group[-1]})" if group else f"Grupo {g_idx+1}"
        group_buttons.append(dict(
            label=label,
            method="update",
            args=[
                {"visible": vis},
                {"title": f"Distribución por Objeto — {label}"}
            ]
        ))

    fig.update_layout(
        updatemenus=[
            dict( 
                type="dropdown",
                x=1.0, y=1.2, xanchor="left", yanchor="top",
                showactive=True,
                buttons=metric_buttons
            ),
            dict( 
                type="dropdown",
                x=1.0, y=1.05, xanchor="left", yanchor="top",
                showactive=True,
                buttons=group_buttons
            )
        ],
        title=f"Distribución por Objeto — Grupo 1 ({object_id_groups[0][0]} - {object_id_groups[0][-1]})" if object_id_groups[0] else "Distribución por Objeto",
        xaxis_title="Object ID",
        yaxis_title="Valor (nb_point / confidence)",
        showlegend=False,
        height=600 
    )

    return fig

