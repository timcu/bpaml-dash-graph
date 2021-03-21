import pandas as pd
import numpy as np
import plotly
import plotly.graph_objects as go

from plotly.subplots import make_subplots

import utilities


def fig_for_location(data, country=None, state=None, num_start=100, case_type="confirmed", averaged_days=5,
                     yaxes_type='log'):
    """Creates a plotly Figure showing COVID-19 cases since count reached num_start
    Plotted on a logarithmic scale
    Also shows calculated number of days to double averaged over the last number of days
    Description describes which data set is being used, confirmed, recovered, deaths
    """
    series_sum = data.series_sum_for_location(case_type=case_type, country=country, state=state)
    if len(series_sum) == 0:
        # most likely cause is someone has selected country and current state is not in that country
        state = None
        series_sum = data.series_sum_for_location(case_type=case_type, country=country, state=state)
    df_sum = pd.DataFrame({"current": series_sum})
    idx_start = df_sum['current'].index[df_sum['current'] >= num_start][0]
    df_sum['previous'] = df_sum['current'].shift(averaged_days, fill_value=0)
    df_plot = df_sum.loc[idx_start:].copy()
    df_plot['doubling days'] = averaged_days / np.log2(df_plot['current'] / df_plot['previous'])
    location = utilities.location_name(country=country, state=state)
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True,
        specs=[[{"rowspan": 2}], [None], [{}]],
        subplot_titles=[f"{case_type.title()} cases on a {yaxes_type} scale",
                        f"Days to double averaged over last {averaged_days} days."]
    )
    fig.update_layout(
        title_text=f"{case_type.title()} cases {location} starting from {num_start}",
        height=600
    )
    trace_type = ""
    fig.add_trace(
        go.Scatter(x=df_plot.index, y=df_plot['current'], mode='lines', name=location + trace_type),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df_plot.index, y=df_plot['doubling days'], mode='lines', showlegend=False),
        row=3, col=1
    )
    fig.update_yaxes(title_text='Cases', type=yaxes_type, row=1, col=1)
    fig.update_layout(legend_traceorder="normal")
    for doubler in (4, 5, 6, 8, 10, 12):
        num_start_actual = df_plot.loc[idx_start, 'current']
        legend = f'every {doubler} days'
        df_plot[legend] = num_start_actual * np.exp2((df_plot.index - idx_start).days / doubler)
        fig.add_trace(
            go.Scatter(x=df_plot.index, y=df_plot[legend], mode='lines', name=legend),
            row=1, col=1
        )
    return fig
