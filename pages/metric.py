import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template='/metric/<metric>')
from dash.dash_table import FormatTemplate
import plotly.express as px

from data import df, df_detail

def layout(metric = None):
    metric_bar = dbc.Row(
        [
            dcc.Dropdown(
                id="selected_metric",
                options = [{'label': i, 'value': i} for i in sorted(df.metric.unique())],
                multi=False,
                value=metric,
                placeholder="Select a metric",
                className=".dropdown",
                style={
                    'width': "40%",
                    'color': 'gray'
                },
            ),
        ],
        #className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
        align="center",
    )
        
    return html.Div([
        html.H2(children=[ "Metric" ]),
        metric_bar,
        dcc.Graph(id='metric_compliance_trend', figure={}),
        html.H2(children=[ "Evidence" ] ),
        dbc.Row([
            dcc.Dropdown(
                id="selected_compliance",
                options = [{'label': 'Non-Compliance', 'value': 0},
                           {'label': 'Compliance', 'value': 1}],
                multi=False,
                value='',
                placeholder="Select Compliance state",
                className=".dropdown",
                style={
                    'width': "40%",
                    'color': 'gray'
                },
            )],
            #className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
            align="center",
        ),
        html.Div(id='metric_table', children=[], style = { 'width' : "80%" } )
    ])

@callback(
    [
        Output(component_id='metric_compliance_trend', component_property='figure'),
        Output(component_id='metric_table', component_property='children')
    ],
    [
        Input(component_id='selected_mapping', component_property='value'),
        Input(component_id='selected_metric', component_property='value'),
        Input(component_id='selected_compliance', component_property='value'),
        
    ]
)
def update_graph(selected_mapping,selected_metric,selected_compliance):
    if selected_mapping != None:
        summary = df[df['mapping'] == selected_mapping]
    else:
        summary = df[df['mapping'] == '/']

    trend = summary[summary['metric'] == selected_metric].groupby(['datestamp'],as_index=True)[['compliance']].mean().reset_index()
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
    mytable = df_detail[(df_detail['metric'] == selected_metric) & (df_detail['compliance'] == selected_compliance)]

    tbl = dash_table.DataTable(
        mytable.to_dict('records'),
        columns = [
            dict(id='datestamp', name='Datestamp'),
            dict(id='resource', name='Resource'),
            dict(id='mapping', name='Mapping'),
            dict(id='compliance', name='Compliance', type='numeric', format=FormatTemplate.percentage(0)),
            dict(id='detail', name='Detail'),

        ],
        style_data_conditional = [
            {
                'if': {
                    'filter_query': '{compliance} < 1',
                    'column_id': 'compliance'
                },
                'backgroundColor': 'darkred',
                'color': 'white'
            },
            {
                'if': {
                    'filter_query': '{compliance} = 1',
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