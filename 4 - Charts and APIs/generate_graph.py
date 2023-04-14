import requests
import json
import pandas as pd
import plotly.express as px

response_API = requests.get('https://api.covid19api.com/country/singapore/status/confirmed?from=2020-03-01T00:00:00Z&to=2022-03-01T00:00:00Z')
data = json.loads(response_API.content)

df = pd.DataFrame([{'Date':row['Date'],'Cases':row['Cases']} for row in data])

fig = px.line(df,x = 'Date',y = 'Cases')
fig.write_html('../index.html')