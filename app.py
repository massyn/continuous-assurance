from dash import Dash,dash_table
from dash import dcc
from dash.dash_table import FormatTemplate

import dash_bootstrap_components as dbc

from dash import html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

# ==== TODO ====
# Page 1 - Executive
# -- Hyperlink to page 2

# Page 2 - Technical
# -- show the trend for that metric
# -- Show the latest list of resources to be measured
# -- Filter by metric id, hierarchy, and compliance

# ==================================================

# -- Create more pages  https://community.plotly.com/t/introducing-dash-pages-a-dash-2-x-feature-preview/57775

# ============================================================================

DATALAKE = '_datalake'

detail = pd.read_csv(f"{DATALAKE}/rollup.csv")
detail["datestamp"] = pd.to_datetime(detail["datestamp"],format="%Y-%m-%d")

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div(
    children = [
        html.H1(children="Continuous Assurance",),
        html.P(
            children=[
                "Continuous Assurance Starter App"
            ]
        ),
        dcc.Dropdown(
            id="selected_mapping",
            options = [{'label': i, 'value': i} for i in sorted(detail.mapping.unique())],
            multi=False,
            value="/",
            placeholder="Select a mapping",
            style={
                'width': "40%",
                'color': 'gray'
            },
        ),
        html.H2(children=[ "Executive Overview" ]),
        dcc.Graph(id='overall_compliance_trend', figure={}),
        html.H2(children=[ "List of metrics"] ),
        html.Div(id='output_table', children=[], style = { 'width' : "80%" } )
    ]
)

# Connect the Plotly graphs with Dash Components
@app.callback(
    [
        Output(component_id='overall_compliance_trend', component_property='figure'),
        Output(component_id='output_table', component_property='children')
    ],
    [
        Input(component_id='selected_mapping', component_property='value')
    ]
)

def update_graph(selected_mapping):
    if selected_mapping != None:
        summary = detail[detail['mapping'] == selected_mapping]
    else:
        summary = detail[detail['mapping'] == '/']
    
    trend = summary.groupby(['datestamp'],as_index=True)[['compliance']].mean().reset_index()
    trend.columns = [ 'datestamp' , 'compliance']
    
    fig = px.line(
        data_frame=trend,
        x='datestamp',
        y='compliance',
        markers=True,
        template='plotly_dark'
    )
    fig.update_layout(
        yaxis=dict(
            tickformat = ".0%",
            range = [ 0 , 1 ],
            title = "Compliance"
        ),
        xaxis=dict(
            title = 'Timeframe'
        )
    )
    
    # -- build the metric table
    mytable = summary[summary['datestamp'] == summary['datestamp'].max()].groupby(['metric','datestamp'],as_index=True)[['compliance']].mean().reset_index()

    tbl = dash_table.DataTable(
        mytable.to_dict('records'),
        columns = [
            dict(id='metric', name='Metric'),
            dict(id='datestamp', name='Datestamp'),
            dict(id='compliance', name='Compliance', type='numeric', format=FormatTemplate.percentage(2))
        ],
        style_data_conditional = [
            {
                'if': {
                    'filter_query': '{compliance} < 0.9',
                    'column_id': 'compliance'
                },
                'backgroundColor': 'darkred',
                'color': 'white'
            },
            {
                'if': {
                    'filter_query': '{compliance} >= 0.9',
                    'column_id': 'compliance'
                },
                'backgroundColor': 'lawngreen',
                'color': 'black'
            }

        ],
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white'
        },
        style_data={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        }
    )

    return fig, tbl

if __name__ == '__main__':
    app.run_server(debug=True)