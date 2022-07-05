import os
import plotly.express as px


def map_scatter(data=clustered_data, latitude='latitude', longitude='longitude', hover_name='neighborhood', color='cluster')
    # Define mapbox token
    maptoken = os.environ["MAPBOX_TOKEN"]

    # plot points and color by cluster
    fig = px.scatter_mapbox(data, lat=latitude, lon=longitude, hover_name=hover_name, color=color,
                            height=500)
    fig.update_geos(fitbounds="locations")
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=maptoken, margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()