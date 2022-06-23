## Description
This project was born from my personal need to monitor my network speed to pinpoint the moments when the internet access was interrupted. The graphs created by this project were used as evidence that there is something wrong with the network access, evidence that was used to report this issue to the service provider, who eventually changed their router, fixing my issue.

## How it works:
* The script can be scheduled, using Task Scheduler in Windows, so that it starts at logon. It will collect the Download and Upload speed of your connection, each 2 minutes (can be configured to other sample rates).
* The script can also be started manually
* Additionally to the data collection script, there is a "make_graph.py" script that will take those exported data points and plot them using Bokeh.

Here is an example: 
![Example](/sample_img.png)