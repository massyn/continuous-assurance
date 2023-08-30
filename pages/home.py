import dash
from dash import html, dcc, callback, Input, Output, dash_table
from dash.dash_table import FormatTemplate
import plotly.express as px

dash.register_page(__name__, path='/')

from data import df

layout = html.Div([
    html.H2(children=[ "Executive Overview" ]),
    dcc.Graph(id='overall_compliance_trend', figure={}),
    html.H2(children=[ "List of metrics"] ),
    html.Div(id='output_table', children=[], style = { 'width' : "80%" } )
])

# Connect the Plotly graphs with Dash Components
@callback(
    [
        Output(component_id='overall_compliance_trend', component_property='figure'),
        Output(component_id='output_table', component_property='children')
    ],
    [
        Input(component_id='selected_mapping', component_property='value')
    ]
)

def update_graph(selected_mapping):
    def create_hyperlink(reference):
        return f'[{reference}](/metric/{reference})'
    
    if selected_mapping != None:
        summary = df[df['mapping'] == selected_mapping]
    else:
        summary = df[df['mapping'] == '/']
    
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

    mytable['metric'] = mytable['metric'].apply(create_hyperlink)

    tbl = dash_table.DataTable(
        mytable.to_dict('records'),
        columns = [
            dict(id='metric', name='Metric', presentation = 'markdown'),
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