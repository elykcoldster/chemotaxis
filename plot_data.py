import plotly

import numpy as np

plotly.tools.set_credentials_file(username='easwaran6192', api_key='hoNKkTAaHj3mUdBHEm1x')

reorientAndBearing = np.loadtxt('reorientation_speed_and_bearing.txt', delimiter = ",")

trace = plotly.graph_objs.Scatter(
    x = reorientAndBearing[:,0],
    y = reorientAndBearing[:,1],
    mode = 'markers'
)

data = [trace]

# Plot and embed in ipython notebook!
plotly.plotly.iplot(data, filename='stats_dump/reorient_and_bearing')