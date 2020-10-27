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

# To find the proper path to find the html file we want to display
import os



# Takes a filename and generates the map requested by the user
def generateMap( dirName, fName ) :
  # Reads in the info from our COVID data set
  #df = pd.read_csv("./cases/Cases-4-7-20vs4-8-20-intDays7/ALL-CommID-Cases-4-7-20vs4-8-20-intDays7.csv",
  #                    dtype={"fips": str}, encoding='latin-1')
  #df = pd.read_csv("../../Cases-4-7-20vs4-8-20_HighSchoolDiploma.csv",
  #                    dtype={"fips": str}, encoding='UTF-8')

  """
  TODO: Create a way to parse a folder from filename

  """
  path = ( './cases/'+ dirName + 
           '/' + fName + '.csv' )

  df = pd.read_csv(path, dtype={"fips": str}, encoding='UTF-8')

  # Creates the map object and fills it with 
  #   information
  fig = px.choropleth(df, geojson=counties, locations='fips', color='CommunityID',
                             # color_continuous_scale=px.colors.diverging.RdYlGn[::-1],
                             color_continuous_scale=px.colors.sequential.OrRd,
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
  #fig.show()
 
  # Path to the specific directory the file is stored in 
  nDir  = ( './graphs/' + dirName + '/' )

  # Path to where to store the file for the hash table
  nFile = fName + '.html'

  # Creates an html file of the map
  pio.write_html(fig, file= nDir + nFile, auto_open=False)

  return fig
#-------------------------------------------------------------



# Takes user input to determine what type of map to generate
#
# Will delete once we get GUI finalized
#   TODO: Use GUI input
def readOpt() :
  options = []

  with open( './cases/Covid19Period.conf', 'r' ) as fp :
    lines = fp.read().replace( '\r', '' ).split( '\n' )

  for line in lines :
    if not line.startswith( '#', 0, len(line) ) :
      options.append(line)

  return options
#-------------------------------------------------------------



# Initializes the CSV Hash Table
def initCSVHash() :
  # The dictionary that stores all the keys to
  #   the csv file we want to generate maps from
  csvHash = {}

  with open( './tables/csv_table.txt', 'r' ) as fp :
    lines = fp.read().replace( '\r', '' ).split( '\n' )

  # Checks if the file is not empty
  if lines[0] != '' :
    for line in lines :
      line = line.split( ',' )

      key = line[0]
      val = line[1]

      csvHash[key] = val
  
  return csvHash
#-------------------------------------------------------------



# Initializes the Map Hash Table
def initMapHash() : 
  # The dictionary that stores all the keys to
  #   the html file we want to display to the
  #   home page iframe
  mapHash = {}

  with open( './tables/html_table.txt', 'r' ) as fp :
    lines = fp.read().replace( '\r', '' ).split( '\n' )

  fp.close()

  # Checks if the file is not empty
  if lines[0] != '' :
    for line in lines :
      line = line.split( ',' )

      key = line[0]
      val = line[1]

      mapHash[key] = val

  return mapHash
#-------------------------------------------------------------



# Formats the key of the hash table to be similar
#   the names of all the .csv and .html files 
def createKey( tempKey ) :
  key = ''

  if( tempKey.endswith('ALL') ) :
    # Holds the ALL part of the string to be moved
    #   to the front of a key
    front = tempKey[-3:]

    # Rearranges the string for key in order for
    #   it to fit the format of each files that
    #   will need to be read in
    middle = tempKey[1:-3]

    end    = tempKey[:1]

    key = front + middle + end
  else :
    # Otherwise, last element in the key will be 
    #   a single digit
    front = tempKey[-1:]

    middle = tempKey[1:-1]

    end = tempKey[:1]

    key = front + middle + end

  return key
#-------------------------------------------------------------


def main() :
  mapHash = initMapHash()
  csvHash = initCSVHash()

  # Reads in user input from a configuration file
  options = readOpt()

  # Stores the name of the temporary key
  tempKey = ''

  # Creates a key using the user input
  for i in range( len(options) ) :
    tempKey = tempKey + options[i] 

    # Separates each element in the key by a hyphen
    if i != len(options) - 1 :
      tempKey = tempKey + '-' 

  # Reformats the key to be easier to read with the file names
  key = createKey( tempKey )

  # Each element is separated into
  keys = key.split( '-' )

  # Concatenates the strings that will be used for filename
  fName = ( keys[0] + '-CommID-Cases-' +
            keys[1] + '-' + keys[2] + '-' +
            keys[3] + 'vs' + keys[4] + '-' +
            keys[5] + '-' + keys[6] + 
            '-intDays' + keys[7] )
    
  # Creates a subdirectory for the data set if it doesn't exist
  subName = ( 'Cases-'+ keys[1] + '-' +
              keys[2] + '-' + keys[3] + 
              'vs' + keys[4] + '-' +
              keys[5] + '-' + keys[6] + 
              '-intDays' + keys[7] )

  # Check if there is a map for this dataset
  if mapHash.get( key ) != None :
    print( "key: %s does exist" % key )
    fName = './graphs/' + subName + '/' + mapHash[key]
    print(fName)
  else :
    print( "key: %s doesn't exist" % key )

    # Creates the path for where to store the file
    path = os.getcwd() + '/graphs/'+ subName
    
    # Checks if a directory for the data set exists
    # If not, then we create one
    if not os.path.isdir( path ) :
      try :
        os.mkdir(path)
      except OSError :
        print ("Mkdir for directory %s has failed." % path)

    fig = generateMap( subName, fName )

    # Add key and value to the HTML hash table 
    with open( './tables/html_table.txt', 'a' ) as fp :
      fp.write( key + ',' + fName + '.html' )

    fp.close()
#-------------------------------------------------------------


if ( __name__ == '__main__' ) :
  main()
