import pandas as pd
import plotly.graph_objects as go

def create_bar_with_lines_chart(df: pd.DataFrame, window: int = 3) -> go.Figure:
    """
    Opción 1:
      - Barras: valor por timestamp (si hay >1 objeto en un timestamp, usa el promedio).
      - Línea: media móvil (ventana = window).
      - Banda: ±1 desviación estándar móvil (ventana = window).
      - Dropdown: nb_point / confidence.
    Requiere columnas: ['timestamp','object_id','nb_point','confidence'].
    """

    required = {"timestamp", "object_id", "nb_point", "confidence"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas en df: {missing}")

    # Asegurar orden temporal
    dfp = df.copy()
    dfp = dfp.sort_values(["timestamp", "object_id"])

    def prep(metric: str):
        # Promedio por timestamp (por si llegan duplicados u >1 objeto; para 1 objeto, es el propio valor)
        s = (pd.to_numeric(dfp[metric], errors="coerce")
               .groupby(dfp["timestamp"])
               .mean()
               .sort_index())
        rmean = s.rolling(window=window, min_periods=1).mean()
        rstd  = s.rolling(window=window, min_periods=1).std(ddof=1).fillna(0.0)
        upper = rmean + rstd
        lower = rmean - rstd
        return s.index.tolist(), s.tolist(), rmean.tolist(), upper.tolist(), lower.tolist()

    # Precalcular para ambas métricas
    x_nb, y_nb, mean_nb, up_nb, lo_nb = prep("nb_point")
    x_cf, y_cf, mean_cf, up_cf, lo_cf = prep("confidence")

    # --- Figura inicial: nb_point ---
    fig = go.Figure()

    # Barras
    fig.add_trace(go.Bar(
        x=x_nb, y=y_nb, name="Valor (NV Points)",
        marker_color="#1f77b4",
        hovertemplate="timestamp=%{x}<br>valor=%{y}<extra></extra>"
    ))

    # Banda inferior (traza 'base' para rellenar hasta la superior)
    fig.add_trace(go.Scatter(
        x=x_nb, y=lo_nb, name="Banda -1σ", mode="lines",
        line=dict(width=0), showlegend=False, hoverinfo="skip"
    ))
    # Banda superior con fill a la traza previa
    fig.add_trace(go.Scatter(
        x=x_nb, y=up_nb, name="±1σ (móvil)", mode="lines",
        line=dict(width=0), fill="tonexty", fillcolor="rgba(31,119,180,0.15)",
        hovertemplate="timestamp=%{x}<br>±1σ=[%{y:.3f}, prev]<extra></extra>"
    ))

    # Línea media móvil
    fig.add_trace(go.Scatter(
        x=x_nb, y=mean_nb, name="Media móvil (NV Points)",
        mode="lines+markers", line=dict(width=2, color="#9467bd"),
        marker=dict(size=6),
        hovertemplate="timestamp=%{x}<br>media_móvil=%{y:.3f}<extra></extra>"
    ))

    # Dropdown: cambiar a Confidence / volver a NV Points
    # Cambiamos Y (y X por si difieren), nombres y título.
    buttons = [
        dict(
            label="NV Points (nb_point)",
            method="update",
            args=[
                {
                    "x": [x_nb, x_nb, x_nb, x_nb],
                    "y": [y_nb, lo_nb, up_nb, mean_nb],
                    "name": ["Valor (NV Points)", "Banda -1σ", "±1σ (móvil)", "Media móvil (NV Points)"]
                },
                {"title": f"Por timestamp — Barras: valor | Línea: media móvil {window} | Banda: ±1σ (NV Points)"}
            ]
        ),
        dict(
            label="Confidence",
            method="update",
            args=[
                {
                    "x": [x_cf, x_cf, x_cf, x_cf],
                    "y": [y_cf, lo_cf, up_cf, mean_cf],
                    "name": ["Valor (Confidence)", "Banda -1σ", "±1σ (móvil)", "Media móvil (Confidence)"]
                },
                {"title": f"Por timestamp — Barras: valor | Línea: media móvil {window} | Banda: ±1σ (Confidence)"}
            ]
        ),
    ]

    fig.update_layout(
        updatemenus=[dict(
            type="dropdown", buttons=buttons, showactive=True,
            x=1.02, y=1.15, xanchor="left", yanchor="top"
        )],
        title=f"Por timestamp — Barras: valor | Línea: media móvil {window} | Banda: ±1σ (NV Points)",
        xaxis_title="timestamp",
        yaxis_title="valor",
        template="plotly_white",
        margin=dict(l=40, r=20, t=80, b=40),
        hovermode="x unified"
    )

    return fig
