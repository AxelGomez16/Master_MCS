import pandas as pd
import plotly.graph_objects as go

ruta_mexico_csv = "mexico/casos_semanales_mexico_2020-2023.csv"
ruta_filipinas_csv = "filipinas/casos_semanales_filipinas_2020-2023.csv"

COLUMNA_CASOS = 'Weekly cases'

def procesar_datos_pais(ruta_archivo, pais_nombre):
    
    print(f"Procesando datos para {pais_nombre} desde '{ruta_archivo}'...")
    df = pd.read_csv(ruta_archivo)
    df['Day'] = pd.to_datetime(df['Day'])
    df['Mes'] = df['Day'].dt.to_period('M')
    
    df_mensual = df.groupby('Mes')[COLUMNA_CASOS].sum().reset_index()
    df_mensual.rename(columns={COLUMNA_CASOS: f'Casos_{pais_nombre}'}, inplace=True)
    
    df_mensual[f'Media_Movil_{pais_nombre}'] = df_mensual[f'Casos_{pais_nombre}'].rolling(window=3, center=True).mean()
    
    return df_mensual

try:
    df_mexico = procesar_datos_pais(ruta_mexico_csv, "Mexico")
    df_filipinas = procesar_datos_pais(ruta_filipinas_csv, "Filipinas")

    df_final = pd.merge(df_mexico, df_filipinas, on='Mes', how='outer').fillna(0)
    df_final['Mes'] = df_final['Mes'].dt.to_timestamp()
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_final['Mes'], 
        y=df_final['Casos_Mexico'],
        fill='tozeroy',
        mode='none',
        name='Casos Mensuales (México)',
        fillcolor='rgba(31, 119, 180, 0.3)'
    ))
    fig.add_trace(go.Scatter(
        x=df_final['Mes'],
        y=df_final['Media_Movil_Mexico'],
        mode='lines',
        name='Tendencia (México)',
        line=dict(color='rgba(31, 119, 180, 1.0)', width=3)
    ))

    fig.add_trace(go.Scatter(
        x=df_final['Mes'],
        y=df_final['Casos_Filipinas'],
        fill='tozeroy',
        mode='none',
        name='Casos Mensuales (Filipinas)',
        fillcolor='rgba(255, 127, 14, 0.3)'
    ))
    fig.add_trace(go.Scatter(
        x=df_final['Mes'],
        y=df_final['Media_Movil_Filipinas'],
        mode='lines',
        name='Tendencia (Filipinas)',
        line=dict(color='rgba(255, 127, 14, 1.0)', width=3)
    ))

    fig.update_layout(
        title_text='<b>Tendencia Comparativa de Casos de COVID-19: México vs. Filipinas</b>',
        xaxis_title='Mes',
        yaxis_title='Casos Nuevos Reportados',
        xaxis_dtick="M1",
        legend_title_text='Métricas y País',
        template='plotly_white',
        hovermode="x unified"
    )

    ruta_grafico = "grafico_comparativo_casos.html"
    fig.write_html(ruta_grafico)

    print(f"\n Grafico guardado en: {ruta_grafico}")

except FileNotFoundError as e:
    print(f"\n No se encontro el archivo '{e.filename}'")
except KeyError:
    print(f"\n No se encontró la columna de casos '{COLUMNA_CASOS}'")
except Exception as e:
    print(f"\n Ocurrió un error inesperado: {e}")