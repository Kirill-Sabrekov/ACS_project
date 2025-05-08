import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import requests

API_URL = "http://localhost:8000/api/v1/data"

def fetch_data_from_api():
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# 🎨 Dash-приложение с Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "📈 Monitoring Dashboard"

app.layout = dbc.Container([
    html.H2("📡 Мониторинг данных", className="text-center mt-4"),

    dbc.Card([
        dbc.CardHeader("🔎 Фильтры"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Node ID"),
                    dcc.Dropdown(id='filter-nodeid', multi=True, placeholder="Выберите nodeid")
                ], md=4),
                dbc.Col([
                    html.Label("Record Type"),
                    dcc.Dropdown(id='filter-recordtype', multi=True, placeholder="Тип записи")
                ], md=4),
                dbc.Col([
                    html.Label("App ID"),
                    dcc.Dropdown(id='filter-appid', multi=True, placeholder="App ID")
                ], md=4),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    html.Label("Quality"),
                    dcc.Dropdown(id='filter-quality', multi=True, placeholder="Качество")
                ], md=4),
                dbc.Col([
                    html.Label("Временной диапазон"),
                    dcc.DatePickerRange(
                        id='filter-time-range',
                        display_format='YYYY-MM-DD',
                        start_date_placeholder_text='Начало',
                        end_date_placeholder_text='Конец'
                    )
                ], md=8),
            ])
        ])
    ], className="mb-4"),

    dcc.Graph(id='main-graph'),

    dcc.Interval(id='auto-refresh', interval=10*1000, n_intervals=0)  # обновление каждые 10 сек
], fluid=True)


# 🔁 Обновление фильтров динамически
@app.callback(
    Output('filter-nodeid', 'options'),
    Output('filter-recordtype', 'options'),
    Output('filter-appid', 'options'),
    Output('filter-quality', 'options'),
    Input('auto-refresh', 'n_intervals')
)
def update_filter_options(_):
    df = fetch_data_from_api()
    return (
        [{'label': str(i), 'value': str(i)} for i in sorted(df['nodeid'].dropna().unique())],
        [{'label': str(i), 'value': str(i)} for i in sorted(df['recordtype'].dropna().unique())],
        [{'label': str(i), 'value': str(i)} for i in sorted(df['appid'].dropna().unique())],
        [{'label': str(i), 'value': str(i)} for i in sorted(df['quality'].dropna().unique())],
    )


# 📈 Обновление графика
@app.callback(
    Output('main-graph', 'figure'),
    Input('auto-refresh', 'n_intervals'),
    State('filter-nodeid', 'value'),
    State('filter-recordtype', 'value'),
    State('filter-appid', 'value'),
    State('filter-quality', 'value'),
    State('filter-time-range', 'start_date'),
    State('filter-time-range', 'end_date'),
)
def update_graph(_, nodeids, recordtypes, appids, qualities, start_date, end_date):
    print(f"Фильтры: nodeids={nodeids}, recordtypes={recordtypes}, appids={appids}, qualities={qualities}")
    print(f"Временные фильтры: start_date={start_date}, end_date={end_date}")
    
    df = fetch_data_from_api()

    # Преобразуем UUID в строки
    df['appid'] = df['appid'].astype(str)

    # Фильтрация
    if nodeids:
        # Если в фильтре только одно значение, обрабатываем как список
        if isinstance(nodeids, str):
            nodeids = [nodeids]
        df = df[df['nodeid'].isin(nodeids)]

    if recordtypes:
        if isinstance(recordtypes, str):
            recordtypes = [recordtypes]
        df = df[df['recordtype'].isin(recordtypes)]

    if appids:
        if isinstance(appids, str):
            appids = [appids]
        df = df[df['appid'].isin(appids)]

    if qualities:
        if isinstance(qualities, str):
            qualities = [qualities]
        df = df[df['quality'].isin(qualities)]

    if start_date:
        df = df[df['timestamp'] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df['timestamp'] <= pd.to_datetime(end_date)]

    print(f"После фильтрации: {len(df)} строк")

    # Группировка и построение графика
    traces = []
    for nodeid in df['nodeid'].unique():
        node_df = df[df['nodeid'] == nodeid]
        traces.append({
            'x': node_df['timestamp'],
            'y': node_df['valdouble'],
            'type': 'scatter',
            'mode': 'lines+markers',
            'name': f'Node {nodeid}'
        })

    return {
        'data': traces,
        'layout': {
            'title': 'Значения valdouble по времени',
            'xaxis': {'title': 'Время'},
            'yaxis': {'title': 'valdouble'},
            'template': 'plotly_white'
        }
    }


if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)
