import pandas as pd
import plotly.graph_objects as go

ruta_mexico_csv = "mexico/datos_mexico_2020-2023.csv"
ruta_filipinas_csv = "filipinas/datos_filipinas_2020-2023.csv"

COLUMNA_MUERTES = 'Cumulative excess deaths (central estimate)'

def procesar_muertes_pais(ruta_archivo, pais_nombre):
    
    print(f"Procesando datos de exceso de muertes para {pais_nombre}...")
    df = pd.read_csv(ruta_archivo)
    df['Day'] = pd.to_datetime(df['Day'])
    
    df[COLUMNA_MUERTES] = df[COLUMNA_MUERTES].ffill()
    
    df['Mes'] = df['Day'].dt.to_period('M')
    
    df_mensual = df.groupby('Mes')[COLUMNA_MUERTES].last().reset_index()
    df_mensual.rename(columns={COLUMNA_MUERTES: f'Muertes_{pais_nombre}'}, inplace=True)
    df_mensual[f'Muertes_{pais_nombre}'] = df_mensual[f'Muertes_{pais_nombre}'].diff().fillna(0)
    
    df_mensual[f'Media_Movil_{pais_nombre}'] = df_mensual[f'Muertes_{pais_nombre}'].rolling(window=3, center=True).mean()
    
    return df_mensual

try:
    df_mexico = procesar_muertes_pais(ruta_mexico_csv, "Mexico")
    df_filipinas = procesar_muertes_pais(ruta_filipinas_csv, "Filipinas")

    df_final = pd.merge(df_mexico, df_filipinas, on='Mes', how='outer').fillna(0)
    df_final['Mes'] = df_final['Mes'].dt.to_timestamp()
    
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_final['Mes'], 
        y=df_final['Muertes_Mexico'],
        name='Exceso de Muertes (México)',
        marker_color='rgba(214, 39, 40, 0.6)' 
    ))
    fig.add_trace(go.Scatter(
        x=df_final['Mes'],
        y=df_final['Media_Movil_Mexico'],
        mode='lines',
        name='Tendencia (México)',
        line=dict(color='rgba(214, 39, 40, 1.0)', width=3) 
    ))

    fig.add_trace(go.Bar(
        x=df_final['Mes'],
        y=df_final['Muertes_Filipinas'],
        name='Exceso de Muertes (Filipinas)',
        marker_color='rgba(31, 119, 180, 0.6)' 
    ))
    fig.add_trace(go.Scatter(
        x=df_final['Mes'],
        y=df_final['Media_Movil_Filipinas'],
        mode='lines',
        name='Tendencia (Filipinas)',
        line=dict(color='rgba(31, 119, 180, 1.0)', width=3) 
    ))

    fig.update_layout(
        title_text='<b>Comparativo de Exceso de Muertes Mensuales: México vs. Filipinas</b>',
        xaxis_title='Mes',
        yaxis_title='Exceso de Muertes Reportadas',
        xaxis_dtick="M1",
        legend_title_text='Métricas y País',
        template='plotly_white',
        barmode='overlay',
        hovermode="x unified"
    )
    fig.data[2].visible = 'legendonly'

    ruta_grafico = "grafico_comparativo_muertes.html"
    fig.write_html(ruta_grafico)

    print(f"\n grafico guardado en: {ruta_grafico}")

except FileNotFoundError as e:
    print(f"\n No se encontro el archivo '{e.filename}'")
except KeyError:
    print(f"\n No se encontró la columna de casos '{COLUMNA_MUERTES}'")
except Exception as e:
    print(f"\n Ocurrió un error inesperado: {e}")