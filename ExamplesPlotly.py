
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

import numpy as np
import pandas as pd


x = [1,2,3,4,5,6,7,8,9]
y = [1,2,3,4,5,6,7,8,9]

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y))

fig.show()