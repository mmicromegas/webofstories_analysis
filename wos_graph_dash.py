import dash
import visdcc
import pandas as pd
#import dash_core_components as dcc
#import dash_html_components as html

from dash import dcc
from dash import html

from dash.dependencies import Input,Output,State
import sys

output = pd.read_pickle("a_file.pkl")
df = output

# https://stackoverflow.com/questions/35268817/unique-combinations-of-values-in-selected-columns-in-pandas-data-frame-and-count

# count distinct value pairs in dataframe !!

df1 = df.groupby(['Source','Target']).size().reset_index().rename(columns={0:'count'})
df = df1

# df1 = df.value_counts(ascending=True).reset_index(name='count')
#print(df1)

#df1_mask=df1['count']>=20
#filtered_df1 = df1[df1_mask]

#df2_mask=filtered_df1['Source']!='administrator'
#filtered_df2 = filtered_df1[df2_mask]

#df3_mask=filtered_df2['Source'].str.contains('Michael')
#filtered_df3 = filtered_df2[df3_mask]
#df = filtered_df3

print(df)
# https://towardsdatascience.com/visualizing-networks-in-python-d70f4cbeb259

# create app
app = dash.Dash()

# create node_list
node_list = list(set(df['Source'].unique().tolist() +
                     df['Target'].unique().tolist()))

nodes = [{'id': node_name, 'label': node_name,'shape': 'dot','size':7}
         for i, node_name in enumerate(node_list)]

# create edges from df
edges = []
for row in df.to_dict(orient='records'):
    source,target = row['Source'], row['Target']
    edges.append({'id': source + "__" + target,
                  'from': source,
                  'to': target,
                  'width': 2})

# define layout
app.layout = html.Div([visdcc.Network(id='net',
                                      data = {'nodes': nodes, 'edges': edges},
                                      options = dict(height='1200px', width='100%'))])


# define main
if __name__ == '__main__':
    app.run_server(debug=True)