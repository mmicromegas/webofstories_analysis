from jaal import Jaal
from jaal.datasets import load_got
import pandas as pd

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

value_list = ["lambda lambda","lambda n","lambda nucleon","the Sewanee Review","boson","meson","SU(3","Ho","Project 2050","Kumar","Jeff",
              "Arthur","Carl","Jim","Felix","Murray","Jean","Bundy","Nicholas","Steven","Margaret","Sam","Reagan","Murphy","Nick","Maya",
              "Marty","Francis","Glashow 1959--'","Lisa","Keith","Mark","Paul","Frenchman","Lisa","Harry","Robby","Serre","Elaine","Val","PCAC",
              "Mutt","Metropolos","Geoff","Frank","Dick","Geoffrey","Brookhaven","Jack","Wu","Mrs Wu","Robert","Newhaven","Mathematical Method",
              "Harald","Ben","Again Sherk","Urbana","Ward","Glasgow","Benedict","Murph","Dean","Lenin","Mohammed","Burgundy","Stanley",
              "Ramond","Nambu","Shelly","Regge","Garwin","Richard","Shelly","Graham","Rochester","Ambler","Hagana","Maiani","SS Chern",
              "Karl","Aurora","Eric","Lusienne","- Farben","Austria","Aber Ihr","Annalen","David","Mozart","Joe","John","Uncle","Hans",
              "Oberlin","Encyclopaedia Britannica","Mayo Clinic","Express","Ken","B"]
df_mask=~df.Target.isin(value_list) # the tilde leads to reverse boolean mask
filtered_df = df[df_mask]

#df3_mask=filtered_df2['Source'].str.contains('Michael')
#filtered_df3 = filtered_df2[df3_mask]
#df = filtered_df3


df = filtered_df
#print(df[df["Source"] == "Murray Gell-Mann"])
# https://towardsdatascience.com/visualizing-networks-in-python-d70f4cbeb259

# create node_list
node_list = list(set(df['Source'].unique().tolist() +
                     df['Target'].unique().tolist()))

nodes = [{'id': node_name, 'label': node_name,'shape': 'dot','size':7}
         for i, node_name in enumerate(node_list)]

nodes_df = pd.DataFrame(nodes)

# create edges from df
edges = []
for row in df.to_dict(orient='records'):
    source,target = row['Source'], row['Target']
    edges.append({'from': source,
                  'to': target,
                  'weight': 2,
                  'strength': 1})
edges_df = pd.DataFrame(edges)


#print(nodes_df.head())

# load the data
edges, nodes = load_got()

print(edges.head())
print(edges_df.head())

# https://pythonrepo.com/repo/imohitmayank-jaal

# init Jaal and run server
Jaal(edges_df, nodes_df).plot()

