import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc


def load_covid_data():
  df = pd.read_csv(r"C:\Users\Axeel\Documents\GitHub\Master_MCS\1st_Semester\Probabilidad_y_Estadistica\Presentacion_Covid_Mex_Phil\casos_semanales__mexico_filipinas_2020-2023.csv")
  df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')

  # Group weekly (per monday) and sum the cases by day
  df['Week'] = df['Date'].dt.to_period('W').apply(lambda r: r.start_time)
  weekly = df.groupby(['Country', 'Week'])['Cases'].sum().reset_index()

  # Pivot for easier comparison i mean the difference of cases
  pivot = weekly.pivot(index='Week', columns='Country', values='Cases').fillna(0)
  pivot['Difference'] = pivot['Mexico'] - pivot['Philippines']

  return weekly, pivot


def data_summary(week_df):
  mex_color      = '#168c16'
  mex_color_back = '#f0fff0'

  phi_color      = '#3498db'
  phi_color_back = '#f0f8ff'

  mexico_data      = week_df[week_df['Country'] == 'Mexico']
  philippines_data = week_df[week_df['Country'] == 'Philippines']

  # Total cases, just sum of all the cases
  mexico_total      = mexico_data['Cases'].sum()
  philippines_total = philippines_data['Cases'].sum()

  # Mean cases, promedio por semana gg
  mexico_avg      = mexico_data['Cases'].mean()
  philippines_avg = philippines_data['Cases'].mean()

  # Maximum case
  mexico_max      = mexico_data['Cases'].max()
  philippines_max = philippines_data['Cases'].max()


  layout_data_summary = html.Div([

    html.Div([

      # Mexico Column
      html.Div([
        html.H4("Mexico", style={'color': mex_color, 'textAlign': 'center'}),
        html.Div([
          html.Div([
            html.P("Total Cases", style={'fontWeight': 'bold', 'color': mex_color, 'margin': '0'}),
            html.P(f"{mexico_total:,.0f}", style={'fontSize': '24px', 'color': mex_color, 'margin': '0'})
          ], style={'textAlign': 'center', 'padding': '10px', 'backgroundColor': mex_color_back, 'borderRadius': '8px',
                    'margin': '5px'}),

          html.Div([
            html.P("Average Weekly", style={'fontWeight': 'bold', 'color': mex_color, 'margin': '0'}),
            html.P(f"{mexico_avg:,.0f}", style={'fontSize': '20px', 'color': mex_color, 'margin': '0'})
          ], style={'textAlign': 'center', 'padding': '10px', 'backgroundColor': mex_color_back, 'borderRadius': '8px',
                    'margin': '5px'}),

          html.Div([
            html.P("Peak Weekly", style={'fontWeight': 'bold', 'color': mex_color, 'margin': '0'}),
            html.P(f"{mexico_max:,.0f}", style={'fontSize': '20px', 'color': mex_color, 'margin': '0'})
          ], style={'textAlign': 'center', 'padding': '10px', 'backgroundColor': mex_color_back, 'borderRadius': '8px',
                    'margin': '5px'})
        ], style={'display': 'flex', 'justifyContent': 'space-around'})
      ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '15px'}),
      # ----------------------------------------------------------------------------


      # Philippines Column
      html.Div([
        html.H4("Philippines", style={'color': phi_color, 'textAlign': 'center'}),
        html.Div([
          html.Div([
            html.P("Total Cases", style={'fontWeight': 'bold', 'color': phi_color, 'margin': '0'}),
            html.P(f"{philippines_total:,.0f}", style={'fontSize': '24px', 'color': phi_color, 'margin': '0'})
          ], style={'textAlign': 'center', 'padding': '10px', 'backgroundColor': phi_color_back, 'borderRadius': '8px',
                    'margin': '5px'}),

          html.Div([
            html.P("Average Weekly", style={'fontWeight': 'bold', 'color': phi_color, 'margin': '0'}),
            html.P(f"{philippines_avg:,.0f}", style={'fontSize': '20px', 'color': phi_color, 'margin': '0'})
          ], style={'textAlign': 'center', 'padding': '10px', 'backgroundColor': phi_color_back, 'borderRadius': '8px',
                    'margin': '5px'}),

          html.Div([
            html.P("Peak Weekly", style={'fontWeight': 'bold', 'color': phi_color, 'margin': '0'}),
            html.P(f"{philippines_max:,.0f}", style={'fontSize': '20px', 'color': phi_color, 'margin': '0'})
          ], style={'textAlign': 'center', 'padding': '10px', 'backgroundColor': phi_color_back, 'borderRadius': '8px',
                    'margin': '5px'})
        ], style={'display': 'flex', 'justifyContent': 'space-around'})
      ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '15px'})
      # ----------------------------------------------------------------------------

    ], style={'textAlign': 'center'})
  ], style={
    'backgroundColor': 'white',
    'padding': '20px',
    'borderRadius': '10px',
    'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'
  })

  return layout_data_summary


def create_map(week_df):
  latest_week = week_df['Week'].max()
  latest_data = week_df[week_df['Week'] == latest_week]

  fig_map = px.choropleth(
    latest_data,
    locations="Country",
    locationmode="country names",
    color="Cases",
    color_continuous_scale="Viridis",
    title=f"Weekly COVID-19 Cases - Mexico & Philippines"
  )
  fig_map.update_geos(fitbounds="locations", visible=False)
  fig_map.update_layout(margin=dict(l=0, r=0, t=40, b=0))

  return fig_map


def create_time_series_chart(week_diff_df):
  fig_time_series = go.Figure()

  fig_time_series.add_trace(go.Scatter(
    x=week_diff_df.index,
    y=week_diff_df['Mexico'],
    line=dict(color='green', width=2),
    marker=dict(color='green', size=6),
    name="Mexico",
    mode="lines+markers",
    hovertemplate=(
        '<b>Country: Mexico</b><br>' +
        '<br>' +
        'Week: %{x|%Y-%m-%d}<br>' +
        'Weekly Cases: %{y:,}<br>' +
        '<extra></extra>'
    )
  ))

  fig_time_series.add_trace(go.Scatter(
    x=week_diff_df.index,
    y=week_diff_df['Philippines'],
    line=dict(color='blue', width=2),
    marker=dict(color='blue', size=6),
    name="Philippines",
    mode="lines+markers",
    hovertemplate=(
        '<b>Country: Philippines</b><br>' +
        '<br>' +
        'Week: %{x|%Y-%m-%d}<br>' +
        'Weekly Cases: %{y:,}<br>' +
        '<extra></extra>'
    )
  ))

  # Difference bar (Mexico - Philippines)
  fig_time_series.add_trace(go.Bar(
    x=week_diff_df.index,
    y=week_diff_df['Difference'],
    name="Difference (MEX - PHL)",
    opacity=0.4,
    marker_color="gray",
    hovertemplate=(
        'Difference (MEX - PHL)<br>' +
        '<br>' +
        'Week: %{x|%Y-%m-%d}<br>' +
        'Weekly Cases: %{y:,}<br>' +
        '<extra></extra>'
    )
  ))

  # TODO: To mark exactly dates maybe either xmas or vacations
  # fig_time_series.add_vline(
  #   x=pd.to_datetime('2022-01-01'),
  #   line_width=2,
  #   line_dash="dash",
  #   line_color="red",
  #   opacity=0.7
  # )


  fig_time_series.update_layout(
    title="Weekly COVID-19 Cases Comparison: Mexico vs Philippines",
    xaxis_title="Week",
    yaxis_title="Weekly Cases",
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    margin=dict(l=40, r=40, t=80, b=40)
  )

  return fig_time_series


def bibliography():

  biblio = """
  World Health Organization (2025) – processed by Our World in Data. \n
  “Cumulative confirmed cases” [dataset]. World Health Organization, \n
  “COVID-19 Dashboard WHO COVID-19 Dashboard - Daily cases and deaths” [original data].
  """

  layout_bibliography = html.Div([

    html.Div([
      html.P(biblio, style={'textAlign': 'center'}),

    ], style={'textAlign': 'center'})
  ], style={
    'backgroundColor': 'white',
    'padding': '20px',
    'borderRadius': '10px',
    'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'
  })

  return layout_bibliography


def create_cumulative_chart(week_df):
  fig = go.Figure()

  mexico_cumulative = week_df[week_df['Country'] == 'Mexico'].set_index('Week')['Cases'].cumsum()
  philippines_cumulative = week_df[week_df['Country'] == 'Philippines'].set_index('Week')['Cases'].cumsum()

  fig.add_trace(go.Scatter(
    x=mexico_cumulative.index,
    y=mexico_cumulative.values,
    name="Mexico",
    line=dict(color='#2E8B57', width=4),
    fill='tozeroy',
    fillcolor='rgba(46, 139, 87, 0.45)',
    opacity=1,
    hovertemplate=(
        '<b>Country: Mexico</b><br>' +
        '<br>' +
        'Week: %{x|%Y-%m-%d}<br>' +
        'Weekly Cases: %{y:,} M<br>' +
        '<extra></extra>'
    )
  ))

  fig.add_trace(go.Scatter(
    x=philippines_cumulative.index,
    y=philippines_cumulative.values,
    name="Philippines",
    line=dict(color='#1E90FF', width=4),
    fill='tozeroy',
    fillcolor='rgba(30, 144, 255, 0.45)',
    opacity=1,
    hovertemplate=(
        '<b>Country: Philippines</b><br>' +
        '<br>' +
        'Week: %{x|%Y-%m-%d}<br>' +
        'Weekly Cases: %{y:,} M<br>' +
        '<extra></extra>'
    )
  ))


  fig.update_layout(
    title="Cumulative cases Over Time",
    xaxis_title="Week",
    yaxis_title="Cumulative Cases",
    template="plotly_white"
  )

  return fig




def weekly_cases_layout():
  week_cases_df, week_difference_cases_df = load_covid_data()

  data_summ_layout    = data_summary(week_cases_df)                           # Data summary
  fig_map             = create_map(week_cases_df)                             # Map cases
  fig_time_series     = create_time_series_chart(week_difference_cases_df)    # Time series chart
  fig_cumulative      = create_cumulative_chart(week_cases_df)              # Accumulative chart
  bibliography_layout = bibliography()                                        # Bibliography

  background_color_card = '#f8f9fa'

  layout = html.Div([
    # Data Summary Section
    html.Div([
      html.H3("📊 Data Summary", style={'textAlign': 'center', 'color': '#34495e', 'marginBottom': '20px'}),
      data_summ_layout
    ], style={
      'width': '100%',
      'padding': '20px',
      'backgroundColor': background_color_card,
      'marginBottom': '30px'
    }),

    # Map Section
    html.Div([
      html.H3("🗺️ Cases Map", style={'textAlign': 'center', 'color': '#34495e', 'marginBottom': '20px'}),
      dcc.Graph(figure=fig_map)
    ], style={
      'width': '100%',
      'height': '50vh',
      'padding': '20px',
      'backgroundColor': background_color_card,
      'marginBottom': '30px'
    }),

    # Time Series Section
    html.Div([
      html.H3("📈 Time Series", style={'textAlign': 'center', 'color': '#34495e', 'marginBottom': '20px'}),
      dcc.Graph(figure=fig_time_series)
    ], style={
      'width': '100%',
      'height': '50vh',
      'padding': '20px',
      'backgroundColor': background_color_card,
      'marginBottom': '30px'
    }),

    # Accumulative Section
    html.Div([
      html.H3("📈 Cumulative cases over time", style={'textAlign': 'center', 'color': '#34495e', 'marginBottom': '20px'}),
      dcc.Graph(figure=fig_cumulative)
    ], style={
      'width': '100%',
      'height': '50vh',
      'padding': '20px',
      'backgroundColor': background_color_card,
      'marginBottom': '30px'
    }),

    # Bibliography Section
    html.Div([
      html.H3("📚 Bibliography", style={'textAlign': 'center', 'color': '#34495e', 'marginBottom': '20px'}),
      bibliography_layout
    ], style={
      'width': '100%',
      'padding': '20px',
      'backgroundColor': background_color_card,
      'marginBottom': '30px'
    }),

  ], style={
    'padding': '20px',
    'backgroundColor': '#ffffff',
    'minHeight': '100vh'
  })

  return layout



