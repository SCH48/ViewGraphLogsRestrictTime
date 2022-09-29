import plotly
import plotly.graph_objs as go

data = [
    ('task 1', 300),
    ('task 2', 1200),
    ('task 3', 500)
]
traces = []
for (key, val) in data:
    traces += [go.Bar(
        x=val,
        y=1,
        name=key,
        orientation='h',
        )]

layout = go.Layout(barmode='stack')
fig = go.Figure(data=traces, layout=layout)
plt.iplot(fig)
