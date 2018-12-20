# -*- coding: utf-8 -*-
import dash
import radial
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import base64
import matplotlib.pyplot as plt

app = dash.Dash()

sample='Iterable,Traversable\nTraversable,Seq\nTraversable,Map\nTraversable,Tree\nTraversable,Iterator\nSeq,IndexedSeq\nSeq,LinearSeq\nIndexedSeq,Array\nIndexedSeq,CharSeq\nIndexedSeq,Vector\nLinearSeq,Stack\nLinearSeq,List\nLinearSeq,Stream\nLinearSeq,Queue\nSet,LinkedHashSet\nSet,HashSet\nSet,SortedSet\nSortedSet,TreeSet\nMap,LinkedHashMap\nMap,HashMap\nMap,SortedMap\nSortedMap,TreeMap'

app.layout = html.Div(children=[
    html.H1(children=u'Draw your radial tree'),
    html.P(children='Insert your tree (make sure of the indexes uniqueness)'),
    # dcc.Input(id='input', type='text'),
    dcc.Textarea(
        id='input',
        placeholder='Insert your tree here',
        value=sample,
        style={'width': '100%'}
    ),
    html.Button('Go', id='button_id'),
    html.P(id='output'),

    # dcc.Graph(
    #     id='example-graph',
    #     figure={
    #         'data': [
    #             {'x': x[3:], 'y': y[3:], 'type': 'line', 'name': 'KEK', 'mode': 'lines'},
    #             {'x': x, 'y': y, 'type': 'line', 'name': 'KEK', 'mode': 'lines'},
    #         ],
    #         'layout': {
    #             'title': 'KEK'
    #             # 'height': 600,
    #             # 'width': 600
    #         }
    #     }
    # )
], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'right'})


def plot_tree(G, arr):
    edges = dict()
    for i in arr:
        edges[i[0]] = []
    for i in arr:
        for j in G:
            if i[0] == j[3] or i[1] == j[3]:
                edges[i[0]].append((j[0], j[1]))

    phi = np.linspace(0, 2*np.pi, 1000)
    plt.clf()
    plt.figure(figsize=(8, 8))

    for key, edge in edges.items():
        x = [i[0] for i in edge]
        y = [i[1] for i in edge]
        for i in range(0, len(edge)):
            plt.plot(x[i: i+2], y[i: i+2], c='black', linestyle='-', marker='o', linewidth=0.5, markersize=3)

    max = 0
    eps = 0.05
    for i in G:
        plt.annotate(i[3], (i[0]+eps, i[1]+eps))
        if max < (i[0]**2 + i[1]**2)**0.5:
            max = (i[0]**2 + i[1]**2)**0.5



    for i in range(int(max)+1):
        plt.plot(i*np.cos(phi), i*np.sin(phi), c='grey', linewidth=0.3)
    plt.axis('off')
    plt.savefig("fig")



@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='button_id', component_property='n_clicks')],
    state=[State(component_id='input', component_property='value')]
)
def on_button(n_clicks, input_data):
    if not input_data is "":
        a = 0
        b = 2 * np.pi
        root, arr = radial.create_tree(input_data)
        G = radial.get_radial_tree(root, a, b)
        plot_tree(G, arr)
        encoded_image = base64.b64encode(open("fig.png", 'rb').read())
        return html.Img(id='img', src='data:image/png;base64,{}'.format(encoded_image.decode()))


if __name__ == '__main__':
    app.run_server(debug=True)
