import requests
import json
import pandas as pd
import plotly.express as px

response_API = requests.get('https://api.covid19api.com/country/singapore/status/confirmed?from=2020-03-01T00:00:00Z&to=2022-03-01T00:00:00Z')
data = json.loads(response_API.content)

# Convert the data from the API call which is in json format into a pandas dataframe for convenient graphing
df = pd.DataFrame([{'Date':row['Date'],'Cases':row['Cases']} for row in data])

# Use plotly express to create a simple interactive graph, then export it to html
fig = px.line(df,x = 'Date',y = 'Cases', title = "Total Confirmed COVID-19 Cases in Singapore Over Time")
fig.write_html('../index.html')