import dash
import visdcc
import pandas as pd
#import dash_core_components as dcc
#import dash_html_components as html

from dash import dcc
from dash import html

import dash_bootstrap_components as dbc # had to install manually dash_bootstrap_components pip install dash_bootstrap_components

from dash.dependencies import Input,Output,State
import sys
import os

filepath = os.path.split(os.path.realpath(__file__))[0]
md_text_head = open(os.path.join(filepath, "mos.md"), "r").read()

output = pd.read_pickle("a_file_mos.pkl")
df = output

# https://stackoverflow.com/questions/35268817/unique-combinations-of-values-in-selected-columns-in-pandas-data-frame-and-count

# count distinct value pairs in dataframe !!

df1 = df.groupby(['Source','Target']).size().reset_index().rename(columns={0:'count'})
df = df1

# df1 = df.value_counts(ascending=True).reset_index(name='count')
#print(df1)

#df1_mask=df1['count']>=20
#filtered_df1 = df1[df1_mask]

value_list = ["lambda lambda"]
df_mask=~df.Target.isin(value_list) # the tilde leads to reverse boolean mask
filtered_df = df[df_mask]

df = filtered_df
#print(df[df["Source"] == "Murray Gell-Mann"])
# https://towardsdatascience.com/visualizing-networks-in-python-d70f4cbeb259

storytellers = df.Source.unique().tolist()

#storytellers = ["Murray Gell-Mann","Aaron Klug","Antony Hewish","Adam Zagajewski"]
storytellers = [{'label': storyteller, 'value': storyteller} for storyteller in storytellers]
#storytellers.insert(0,{'label': 'All storytellers', 'value': 'all_storytellers'})
#storytellers.insert(0,{'label': 'Antony Hewish', 'value':'Antony Hewish'})

# create app
app = dash.Dash()

# define layout
#app.layout = html.Div(
#    html.Div([visdcc.Network(id='net',data = {'nodes': nodes, 'edges': edges},
#                                      options = dict(height='900px', width='100%'))]))

app.layout = html.Div([dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dcc.Markdown(md_text_head, dangerously_allow_html=True)
                ], width=3),
            ], align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Container(children=[
                            # your application content goes here
                            html.Div([
                                html.Div([
                                    html.Label('Storyteller:'),
                                    dcc.Dropdown(
                                        id='storyteller',
                                        options=storytellers,
                                        value='Edward Teller',
                                        multi=True
                                    ),
                                ], style=dict(width='40%')),
                            ], style=dict(display='flex')),
                        ])
                    ])
                ], width=3)], align='center'),
            html.Br(),
            dbc.Row([dbc.Col([html.Div([visdcc.Network(id='net',
             options = dict(height= '800px',
                                    width= '100%',
                                    physics={'barnesHut': {'gravitationalConstant': -8000}, 'springConstant': 0.001, 'springLength': 30},
                                    ))])])], align='left'),
        ])
    )
])

# https://visjs.github.io/vis-network/docs/network/physics.html
#{barnesHut: {gravitationalConstant: -80000, springConstant: 0.001, springLength: 200}}

# update_net
@app.callback(
    Output('net', 'data'),
    [Input('storyteller', 'value')])
def update_net(storytellerSelect):

    if isinstance(storytellerSelect,str):
        storytellerSelect = [storytellerSelect]

    df_mask = df.Source.isin(storytellerSelect)
    df_filter = df[df_mask]

    # create node_list
    node_list = list(set(df_filter['Source'].unique().tolist() +
                         df_filter['Target'].unique().tolist()))

    nodes = [{'id': node_name, 'label': node_name, 'shape': 'dot', 'size': 5}
             for i, node_name in enumerate(node_list)]

    #nodes.remove({'id': False, 'label': False, 'shape': 'dot', 'size': 7})
    #nodes.remove({'id': True, 'label': True, 'shape': 'dot', 'size': 7})
    #nodes.remove({'id': '', 'label': '', 'shape': 'dot', 'size': 7})     # nodes must have id , otherwise error

    #nodes = [{k: v for k, v in d.items() if v != ''} for d in all_nodes]

    # create edges from df_filter
    edges = []
    for row in df_filter.to_dict(orient='records'):
        source, target = row['Source'], row['Target']
        edges.append({'id': source + "__" + target,
                      'from': source,
                      'to': target,
                      'width': 2})

    # clarification
    #nodes = [{'id': 'node1_id', 'label': 'node1_label', 'shape': 'dot', 'size': 7}]
    #nodes.append({'id': 'node2_id', 'label': 'node2_label', 'shape': 'dot', 'size': 7})
    #nodes.append({'id': 'node3_id', 'label': 'node3_label', 'shape': 'dot', 'size': 7})

    #edges = [{'id': 'edge1_id', 'from': 'node1_id', 'to': 'node2_id', 'width': 2}]
    #edges.append({'id': 'edge2_id', 'from': 'node2_id', 'to': 'node3_id', 'width': 2})

    data = {'nodes': nodes, 'edges': edges}

    return data

# define main
if __name__ == '__main__':
    app.run_server(debug=True)