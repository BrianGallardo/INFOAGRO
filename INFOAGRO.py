import dash
from dash import Dash, dcc, html, Input, Output, dash_table, clientside_callback, State, callback, ctx
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import gunicorn

# Carga el archivo CSV
df = pd.read_csv('https://github.com/BrianGallardo/INFOAGRO/blob/8dc1e38a7b1b8ef20276c4476f819193a164a84b/Aguan.csv')

# Establece el índice para que coincida con la imagen
df.set_index('Longitud', inplace=True)

# Grafica de precipitacion
fig = go.Figure()

for col in df.columns:
    fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=col))

fig.update_layout(height=600, width=1200, title='Cuenca Aguan PPD (mm)')

# Carga el archivo CSV
df2 = pd.read_csv('https://github.com/BrianGallardo/INFOAGRO/blob/e02eb54f85773e583d7d1ba1a8fbb5f47ace923a/Cangrejal.csv')

# Establece el índice para que coincida con la imagen
df2.set_index('Longitud', inplace=True)

# Grafica de precipitacion
fig2 = go.Figure()

for col in df2.columns:
    fig2.add_trace(go.Scatter(x=df2.index, y=df2[col], mode='lines', name=col))

fig2.update_layout(height=600, width=1200, title='Cuenca Cangrejal PPD (mm)')

# Carga el archivo CSV
df3 = pd.read_csv('Chamelecon.csv')

# Establece el índice para que coincida con la imagen
df3.set_index('Longitud', inplace=True)

# Grafica de precipitacion
fig3 = go.Figure()

for col in df3.columns:
    fig3.add_trace(go.Scatter(x=df3.index, y=df3[col], mode='lines', name=col))

fig3.update_layout(height=600, width=1200, title='Cuenca Chamelecon PPD (mm)')

# Establece la app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=0.6'}])

# Define la interfaz de usuario
app.layout = html.Div([
    html.H1(["Dashboard INFOAGRO", dbc.Badge("Dashboard INFOAGRO", className="ms-1")]),
    dcc.Graph(id='grafica', figure=fig, selectedData={'points': []}),  # Añade la propiedad selectedData
    dcc.Store(id='selected-data-store', data={'points': []}),  # Almacena los datos seleccionados
    html.Br(),
    dash_table.DataTable(
        id='table-grafica1',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_table={'height': '200px', 'width': '1200px', 'overflowY': 'auto'},
        page_size=8
    ),
    html.Br(),
    dcc.Graph(id='grafica2', figure=fig2, selectedData={'points': []}),  # Añade la propiedad selectedData
    dcc.Store(id='selected-data-store2', data={'points': []}),  # Almacena los datos seleccionados
    html.Br(),
    dash_table.DataTable(
        id='table-grafica2',
        columns=[{"name": i, "id": i} for i in df2.columns],
        data=df2.to_dict('records'),
        style_table={'height': '200px', 'width': '1200px', 'overflowY': 'auto'},
        page_size=8
    ),
    html.Br(),
    dcc.Graph(id='grafica3', figure=fig3, selectedData={'points': []}),  # Añade la propiedad selectedData
    dcc.Store(id='selected-data-store3', data={'points': []}),  # Almacena los datos seleccionados
    html.Br(),
    dash_table.DataTable(
        id='table-grafica3',
        columns=[{"name": i, "id": i} for i in df3.columns],
        data=df3.to_dict('records'),
        style_table={'height': '200px', 'width': '1200px', 'overflowY': 'auto'},
        page_size=8
    ),
    html.Br(),
])

# Devoluciones de llamada para actualizar datos seleccionados y tablas
@app.callback(
    Output('selected-data-store', 'data'),
    Input('grafica', 'selectedData')
)
def update_selected_data(selectedData):
    if selectedData is None:
        selectedData = {'points': []}

    return selectedData

@app.callback(
    Output('table-grafica1', 'data'),
    Input('selected-data-store', 'data')
)
def update_table(selected_data):
    selected_points = selected_data['points']

    if not selected_points:
        # Si no hay puntos seleccionados, muestra todos los datos
        return df.to_dict('records')

    # Filtra los datos basados en los puntos seleccionados
    selected_indices = [point['pointIndex'] for point in selected_points]
    selected_data = df.iloc[selected_indices]

    return selected_data.to_dict('records')

# Repite el proceso para grafica2 y tabla2
@app.callback(
    Output('selected-data-store2', 'data'),
    Input('grafica2', 'selectedData')
)
def update_selected_data2(selectedData):
    if selectedData is None:
        selectedData = {'points': []}

    return selectedData

@app.callback(
    Output('table-grafica2', 'data'),
    Input('selected-data-store2', 'data')
)
def update_table2(selected_data):
    selected_points = selected_data['points']

    if not selected_points:
        # Si no hay puntos seleccionados, muestra todos los datos
        return df2.to_dict('records')

    # Filtra los datos basados en los puntos seleccionados
    selected_indices = [point['pointIndex'] for point in selected_points]
    selected_data = df2.iloc[selected_indices]

    return selected_data.to_dict('records')

# Repite el proceso para grafica3 y tabla3
@app.callback(
    Output('selected-data-store3', 'data'),
    Input('grafica3', 'selectedData')
)
def update_selected_data3(selectedData):
    if selectedData is None:
        selectedData = {'points': []}

    return selectedData

@app.callback(
    Output('table-grafica3', 'data'),
    Input('selected-data-store3', 'data')
)
def update_table3(selected_data):
    selected_points = selected_data['points']

    if not selected_points:
        # Si no hay puntos seleccionados, muestra todos los datos
        return df3.to_dict('records')

    # Filtra los datos basados en los puntos seleccionados
    selected_indices = [point['pointIndex'] for point in selected_points]
    selected_data = df3.iloc[selected_indices]

    return selected_data.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
