# 4 - Charts and APIs

## Problem Statement

Your team decided to design a dashboard to display the statistic of COVID19 cases. You are tasked to display one of the components of the dashboard which is to display a visualisation representation of number of COVID19 cases in Singapore over time.

Your team decided to use the public data from https://documenter.getpostman.com/view/10808728/SzS8rjbc#b07f97ba-24f4-4ebe-ad71-97fa35f3b683.

Display a graph to show the number cases in Singapore over time using the APIs from https://covid19api.com/.

## Solution - Dashboard

The code in `generate_graph.py` was used to create an interactive graph via the package Plotly. Plotly allows zooming in and out of the data visualisation to either specific x-axis or y-axis ranges, and also provides descriptive labels for each data point so that, for example, it is possible to tell exactly what was the total number of Cases at October 21, 2021. Please visit https://t-s-w.github.io/Data-Engineer-Tech-Challenge-Answers/ to have a look!

Alternatively, I also created a Google Data Studio Community Connector for Data Studio to be able to access this API to make conveniently-shareable public dashboards as well. An example dashboard can be seen at https://lookerstudio.google.com/reporting/76b3bb13-2a45-4207-aba1-aced6bfa5e47

![](howto-zoom.png)

![](howto-zoom2.png)