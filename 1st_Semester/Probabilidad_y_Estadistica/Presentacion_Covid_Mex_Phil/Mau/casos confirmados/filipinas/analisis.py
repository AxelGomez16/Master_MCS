import pandas as pd
import plotly.graph_objects as go

ruta_csv = "casos_semanales_filipinas_2020-2023.csv"

try:
    print(f"Cargando datos desde '{ruta_csv}'...")
    df = pd.read_csv(ruta_csv)
    df['Day'] = pd.to_datetime(df['Day'])

    df['Mes'] = df['Day'].dt.to_period('M')
    df_mensual = df.groupby('Mes')['Weekly cases'].sum().reset_index()
    df_mensual.rename(columns={'Weekly cases': 'Casos_Mensuales'}, inplace=True)

    df_mensual['Media_Movil_3M'] = df_mensual['Casos_Mensuales'].rolling(window=3, center=True).mean()
    promedio = df_mensual['Casos_Mensuales'].mean()
    
    df_mensual['Mes'] = df_mensual['Mes'].dt.to_timestamp()
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_mensual['Mes'], 
        y=df_mensual['Casos_Mensuales'],
        fill='tozeroy',  
        mode='none',     
        name='Casos Mensuales',
        fillcolor='rgba(31, 119, 180, 0.3)' 
    ))

    fig.add_trace(go.Scatter(
        x=df_mensual['Mes'],
        y=df_mensual['Media_Movil_3M'],
        mode='lines',
        name='Tendencia (Media Móvil 3 Meses)',
        line=dict(color='#d62728', width=3) 
    ))

    fig.add_trace(go.Scatter(
        x=[df_mensual['Mes'].min(), df_mensual['Mes'].max()],
        y=[promedio, promedio],
        mode='lines',
        name=f'Promedio ({promedio:,.0f})',
        line=dict(color='gray', width=2, dash='dash')
    ))
    
    pico_maximo = df_mensual.loc[df_mensual['Casos_Mensuales'].idxmax()]
    fig.add_annotation(
        x=pico_maximo['Mes'], 
        y=pico_maximo['Casos_Mensuales'],
        text=f"Pico Máximo<br>{pico_maximo['Mes'].strftime('%b %Y')}<br>{pico_maximo['Casos_Mensuales']:,.0f} casos",
        showarrow=True, arrowhead=1, arrowcolor="black",
        ax=0, ay=-80, bordercolor="#c7c7c7", borderwidth=1,
        bgcolor="rgba(255, 255, 255, 0.85)"
    )
    
    fig.update_layout(
        title_text='<b>Tendencia de Casos de COVID-19 en Filipinas</b><br><sup>Casos mensuales reportados y línea de tendencia (2020-2023)</sup>',
        xaxis_title='Mes',
        yaxis_title='Casos Nuevos Reportados',
        xaxis_dtick="M1", 
        template='plotly_white',
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.7)')
    )

    ruta_grafico = "grafico_casos_filipinas.html"
    fig.write_html(ruta_grafico)

    print(f"\n grafico completo guardado en: {ruta_grafico}")
    
except FileNotFoundError:
    print(f"ERROR: archivo no encontrado'{ruta_csv}'.")
except KeyError as e:
    print(f"ERROR: columna perdida {e}, revisar los nombres de las columnas.")
except Exception as e:
    print(f"error inesperado: {e}")