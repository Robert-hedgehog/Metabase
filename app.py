from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()
server = app.server

# Requires Dash 2.17.0 or later
app.layout = [
    html.Div([
        html.Div([
            html.H2(children='Линейный график', style={'textAlign':'center'}),
            dcc.Dropdown(df.country.unique(), value=['Canada', 'United States'], id='dropdown-selection', multi=True),
            html.Div(className='row', children=[
                dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'],
                            value='lifeExp',
                            inline=True,
                            id='my-radio-buttons-final',
                            labelStyle={'fontWeight': 'bold'})
            ],style={'textAlign': 'center'}), 
            dcc.Graph(id='graph-content', style={'height': '35vh'}), 
        ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        html.Div([
            html.H2(id='bubble-title', children='Пузырьковая диаграмма', style={'textAlign':'center'}),
            html.Div([
                html.Div([
                    html.Label('Ось X:'),
                    dcc.Dropdown(options=['pop', 'lifeExp', 'gdpPercap'], value='pop', id='bubble-x', clearable=False)
                ], 
                style={'width': '30%', 'display': 'inline-block', 'marginLeft': '3%'}),
                
                html.Div([
                    html.Label('Ось Y:'),
                    dcc.Dropdown(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='bubble-y', clearable=False)
                ], 
                style={'width': '30%', 'display': 'inline-block', 'marginLeft': '3%'}),
                
                html.Div([
                    html.Label('Радиус:'),
                    dcc.Dropdown(options=['pop', 'lifeExp', 'gdpPercap'], value='gdpPercap', id='bubble-size', clearable=False)
                ], 
                style={'width': '30%', 'display': 'inline-block', 'marginLeft': '3%'}),
            ]), 
            html.Div([dcc.Graph(id='bubble-chart', style={'height': '35vh'})], style={'width': '100%'}),

        ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    ], style={'width': '100%'}),

    html.Div([

        # 3. Топ-15 стран
        html.Div([
            html.H2(id='bar-title', children='Топ-15 стран по популяции', style={'textAlign':'center'}),
            html.Div([dcc.Graph(id='bar-chart-top15', style={'height': '38vh'})], style={'width': '100%'}),
        ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        # 4. Круговая диаграмма
        html.Div([
            html.H2(id='pie-title', children='Круговая диаграмма по популяциям на континентах', style={'textAlign':'center'}),
            html.Div([dcc.Graph(id='pie-chart-continents', style={'height': '38vh'})], style={'width': '100%'}),
        ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    ], style={'width': '100%'})

]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)

def update_line_graph(countries_list, y_axis_name):
    dff = df[df.country.isin(countries_list)]
    fig = px.line(dff, x='year', y=y_axis_name, color='country', markers=True)
    fig.update_layout(margin=dict(l=20, r=20, t=10, b=20))
    return fig

@callback(
    Output('bubble-chart', 'figure'),
    Output('bar-chart-top15', 'figure'),
    Output('pie-chart-continents', 'figure'),
    Output('bubble-title', 'children'),
    Output('bar-title', 'children'),
    Output('pie-title', 'children'),
    Input('graph-content', 'clickData'),
    Input('bubble-x', 'value'),
    Input('bubble-y', 'value'),
    Input('bubble-size', 'value')
)

def update_three_charts(clickData, x_val, y_val, size_val):
    if clickData is None:
        selected_year = 2007
    else:
        selected_year = clickData['points'][0]['x']

    dff = df[df.year == selected_year]

    fig_bubble = px.scatter(
        dff,
        x=x_val,
        y=y_val,
        size=size_val,
        color='continent',
        hover_name='country',
        size_max=40,
        log_x=True if x_val in ['pop', 'gdpPercap'] else False)
    
    fig_top15 = px.bar(dff.nlargest(15, 'pop'), x='country', y='pop', color='continent')
    fig_top15.update_layout(xaxis={'categoryorder':'total descending'})
    
    fig_pie = px.pie(dff, values='pop', names='continent')
    fig_pie.update_layout(legend_title_text='continents')

    fig_bubble.update_layout(margin=dict(l=20, r=20, t=10, b=20))
    fig_top15.update_layout(margin=dict(l=20, r=20, t=10, b=20))
    fig_pie.update_layout(margin=dict(l=20, r=20, t=10, b=20))
    
    bubble_title = f'Пузырьковая диаграмма ({selected_year})'
    bar_title = f'Топ-15 стран по популяции ({selected_year})'
    pie_title = f'Круговая диаграмма по популяциям ({selected_year})'
    
    return fig_bubble, fig_top15, fig_pie, bubble_title, bar_title, pie_title

if __name__ == '__main__':
    app.run(debug=True)