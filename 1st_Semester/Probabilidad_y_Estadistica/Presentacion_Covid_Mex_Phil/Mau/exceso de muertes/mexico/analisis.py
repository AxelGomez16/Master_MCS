import pandas as pd
import plotly.graph_objects as go

ruta_csv = "datos_mexico_2020-2023.csv"

try:
    print(f"agarrando datos desde '{ruta_csv}'...")
    df = pd.read_csv(ruta_csv)
    df['Day'] = pd.to_datetime(df['Day'])

    columna_muertes = 'Cumulative excess deaths (central estimate)'
    df[columna_muertes] = df[columna_muertes].ffill()
    df['Mes'] = df['Day'].dt.to_period('M')
    df_mensual = df.groupby('Mes')[columna_muertes].last().reset_index()
    df_mensual.rename(columns={columna_muertes: 'Total_Acumulado'}, inplace=True)
    df_mensual['Incremento_Mensual'] = df_mensual['Total_Acumulado'].diff().fillna(0)
    
    df_mensual['Mes'] = df_mensual['Mes'].dt.to_timestamp()

    promedio = df_mensual['Incremento_Mensual'].mean()
    mediana = df_mensual['Incremento_Mensual'].median()
    desv_est = df_mensual['Incremento_Mensual'].std()
    
    fig = go.Figure()

    y_upper = [promedio + desv_est] * len(df_mensual)
    y_lower = [promedio - desv_est] * len(df_mensual)
    fig.add_trace(go.Scatter(x=df_mensual['Mes'], y=y_upper, mode='lines', line=dict(width=0), hoverinfo='none', showlegend=False))
    fig.add_trace(go.Scatter(x=df_mensual['Mes'], y=y_lower, mode='lines', line=dict(width=0), fillcolor='rgba(128, 128, 128, 0.2)', fill='tonexty', hoverinfo='none', name='Banda de Desviación Estándar'))

    colors = ['#1f77b4' if x >= 0 else '#d62728' for x in df_mensual['Incremento_Mensual']]
    fig.add_trace(go.Bar(x=df_mensual['Mes'], y=df_mensual['Incremento_Mensual'], name='Incremento Mensual', marker_color=colors))

    fig.add_trace(go.Scatter(x=[df_mensual['Mes'].min(), df_mensual['Mes'].max()], y=[promedio, promedio], mode='lines', name=f'Promedio ({promedio:,.0f})', line=dict(color="#e377c2", width=2, dash="dash")))
    fig.add_trace(go.Scatter(x=[df_mensual['Mes'].min(), df_mensual['Mes'].max()], y=[mediana, mediana], mode='lines', name=f'Mediana ({mediana:,.0f})', line=dict(color="#ff7f0e", width=2, dash="dot")))
    
    pico_maximo = df_mensual.loc[df_mensual['Incremento_Mensual'].idxmax()]
    fig.add_annotation(x=pico_maximo['Mes'], y=pico_maximo['Incremento_Mensual'], text=f"Pico Máximo<br>{pico_maximo['Mes'].strftime('%b %Y')}<br>{pico_maximo['Incremento_Mensual']:,.0f} muertes", showarrow=True, arrowhead=1, arrowcolor="black", ax=0, ay=-80, bordercolor="#c7c7c7", borderwidth=1, borderpad=4, bgcolor="rgba(255, 255, 255, 0.85)")

    fig.update_layout(
        #titulo del grafico
        title_text='<b>Análisis Estadístico del Exceso de Muertes Mensuales en México</b>',
        xaxis_title='Mes',
        yaxis_title='Exceso de Muertes Reportadas',
        xaxis_dtick="M1", 
        template='plotly_white',
        showlegend=True,
        legend=dict(x=0.01, y=0.99)
    )

    ruta_grafico = "grafico_exceso_muertes_mexico.html" 
    fig.write_html(ruta_grafico)

    print(f"\n grafico completo guardado en: {ruta_grafico}")

except FileNotFoundError:
    print(f"ERROR: archivo no encontrado'{ruta_csv}'.")
except KeyError as e:
    print(f"ERROR: columna perdida {e}, revisar los nombres de las columnas.")
except Exception as e:
    print(f"error inesperado: {e}")