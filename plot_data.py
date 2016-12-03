import plotly

import numpy as np

plotly.tools.set_credentials_file(username='easwaran6192', api_key='hoNKkTAaHj3mUdBHEm1x')

reorientAndBearing = np.loadtxt('stats_dump/reorientation_speed_and_bearing.txt', delimiter = ",")

trace = plotly.graph_objs.Scatter(
    x = reorientAndBearing[:,0],
    y = reorientAndBearing[:,1],
    mode = 'markers'
)

data = [trace]

# Plot and embed in ipython notebook!
plotly.plotly.iplot(data, filename='reorient_and_bearing_new_arena')


run_lengths = np.loadtxt('stats_dump/run_lengths.txt')

data = [
    plotly.graph_objs.Histogram(
        x=run_lengths,
        histnorm='probability'
    )
]

plotly.plotly.iplot(data, filename='run_lengths_new_arena')


bearing_freqs_left_turn = np.loadtxt('stats_dump/bearing_freqs_left_turn.txt')

data = [
    plotly.graph_objs.Histogram(
        x=bearing_freqs_left_turn,
        histnorm='probability'
    )
]

plotly.plotly.iplot(data, filename='bearing_freqs_left_turn_new_arena')


absolute_bearing_freqs_turn = np.loadtxt('stats_dump/absolute_bearing_freqs_turn.txt')

data = [
    plotly.graph_objs.Histogram(
        x=absolute_bearing_freqs_turn,
        histnorm='probability'
    )
]

plotly.plotly.iplot(data, filename='absolute_bearing_freqs_turn_new_arena')

absolute_bearing_freqs_turn = np.loadtxt('stats_dump/absolute_bearing_freqs_turn.txt')
