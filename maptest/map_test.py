# Library that gives us the functions to create
#   the map
import plotly.io as pio

# Reads csv files and sorts the states by their
#   fips codes
import pandas as pd

# Object that will be used to execute the 
#   map creation features 
import plotly.express as px

# Reads the map data from a website to help
#   generate the map
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# Reads in the info from our COVID data set
df = pd.read_csv("./cases/Cases-4-7-20vs4-8-20-intDays7/ALL-CommID-Cases-4-7-20vs4-8-20-intDays7.csv",
                    dtype={"fips": str}, encoding='latin-1')

# Creates the map object and fills it with 
#   information
fig = px.choropleth(df, geojson=counties, locations='fips', color='CommunityID',
                           color_continuous_scale=px.colors.diverging.RdYlGn[::-1],
                           range_color=(0, 7),
                           scope="usa",
                           labels={'State':'State',
                                   'Area_Name':'County',
                                   'DensityPerSquaremileOfLandarea-Population':'Pop. Density per Square Mile of Land Area',
                                   'Median_Household_Income_2018':'Median Household Income in 2018',
                                   'Percent_of_adults_with_a_high_school_diploma_only_2014-18':'% Adult with High School Diplomas'}, 
                           hover_data=["Area_Name", "DensityPerSquaremileOfLandarea-Population", 
                                         "Median_Household_Income_2018", 
                                         "Percent_of_adults_with_a_high_school_diploma_only_2014-18"] 
                          )

# Fixes the origin to the right of the map
#   information
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                     coloraxis_colorbar=dict( title = "Percentage Change in the Number of New Cases",
                     ticks = 'inside',
                     tickvals = [0, 1, 2, 3, 4, 5, 6, 7, 8],
                     ticktext=['Drop of Greater than 100%', 'Drop between 50% to 100%', 'Drop between 0% to 50%',
                                'No Change', 'Rise between 0% to 50%', 'Rise between 50% to 100%', 
                                'Rise between 100% to 200%', 'Rise of More than 200%']))

# Displays the figure when program is executed    
fig.show()

# Creates an html file of the map
pio.write_html(fig, file='map.html', auto_open=False)
