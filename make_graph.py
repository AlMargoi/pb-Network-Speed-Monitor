from bokeh.plotting import figure, show, ColumnDataSource, save, output_file
from bokeh.models import HoverTool
from bokeh.layouts import column
from datetime import datetime
import pandas as pd
import time

df = pd.read_csv('.\\network_performance.csv')
for wifi_conn in df['Wifi'].unique():
    wifi_filter = df['Wifi'] == wifi_conn
    filtered_df = df[wifi_filter]
    x_data = pd.to_datetime(filtered_df['time'], dayfirst=True)
    #
    downspeed_CDSData = {
        'datetime': x_data,
        'downspeed': pd.Series(filtered_df['downspeed']),
        'upspeed' : pd.Series(filtered_df['upspeed'])
    }
    downspeed_CDS = ColumnDataSource(downspeed_CDSData)
    #
    #upspeed_CDSData = {
    #    'datetime': x_data,
    #    'upspeed': pd.Series(filtered_df['upspeed']),
    #}
    #upspeed_CDSData = ColumnDataSource(upspeed_CDSData)
    #
    # Create Hover Tool:
    HT = HoverTool(
        tooltips=[
            ('datetime', '@datetime{%F %X}'),
            ('downspeed', '@downspeed{0,0.0}'),
            ('upspeed', '@upspeed{0,0.0}')
        ],
        formatters={
            '@datetime': 'datetime'
        },
    #
        mode='vline',
        names=['pmds']
    )
    # Create the figure:
    net_stats_fig = figure(
        title=f"Download / upload: {wifi_conn}", 
        x_axis_type="datetime",
        x_axis_label="datetime", 
        y_axis_label="Mbps",
        width = 1000,
        height = 350      
    )
    net_stats_fig.add_tools(HT)
    # Add plots:
    if wifi_conn == "Hamburger_1":
        clr1 = "blue"
        clr2 = "red"
    else:
        clr1 = "red"
        clr2 = "green"
    net_stats_fig.circle(x="datetime", y="downspeed", source=downspeed_CDS, size=3, color=clr1, alpha=1)
    net_stats_fig.line(x="datetime", y="downspeed", source=downspeed_CDS, color=clr1, line_width=2, alpha=0.25, name='pmds')
    net_stats_fig.circle(x="datetime", y="upspeed", source=downspeed_CDS, size=3, color=clr2, alpha=1)
    net_stats_fig.line(x="datetime", y="upspeed", source=downspeed_CDS, color=clr2, line_width=2, alpha=0.25)
    output_file(filename=f"{wifi_conn}.html", title="Static HTML file")
    show(net_stats_fig)
    time.sleep(0.5)
