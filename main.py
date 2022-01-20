import pandas as pd
import geopandas as gpd

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

#Read in the required data

elec_2017 = pd.read_csv('2017 presidential election results.csv')
elec_2013 = pd.read_csv('2013 presidential election results.csv')

counties_geojson = gpd.read_file('counties.geojson')

#counties = counties_geojson.merge(elec_2017, on='COUNTY_NAM').set_index("COUNTY_NAM")



#df = px.data.election()
#geojson = px.data.election_geojson()
#candidates = df.winner.unique()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Year:"),
    html.Div(
        dcc.RadioItems(
            id='year',
            options=[{'value': x, 'label': x}
                     for x in [2013,2017]],
            value=2017,
            labelStyle={'display': 'inline-block'})

    ),

    dcc.Graph(id="choropleth"),
])

@app.callback(
    Output("choropleth", "figure"),
    [Input("year", "value")])
def display_choropleth(year):
    if year == 2013:
        counties = counties_geojson.merge(elec_2013, on='COUNTY_NAM').set_index("COUNTY_NAM")
    else:
        counties = counties_geojson.merge(elec_2017, on='COUNTY_NAM').set_index("COUNTY_NAM")
    fig = px.choropleth(
        counties, geojson=counties.geometry, color=counties.Winner,
        locations=counties.index, projection="mercator")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

app.run_server(debug=True)