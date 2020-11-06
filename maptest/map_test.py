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

# Used to import and run the C++ program to generate CSV files
from ctypes import cdll, c_char_p


class map_test() :
  # Constructor
  def __init__( self, interval, sDate, fDate, rates ) :
    # Stores the number of days the user chooses
    self.interval = interval

    # Stores the start date
    self.sDate = sDate

    # Stores the final date
    self.fDate = fDate

    # Stores the rates of change
    self.rates = rates

  # Runs entire checks for generating map
  def main( self ) :
    # Reads in user input from the website
    options = [ self.interval, self.sDate,
                self.fDate, self.rates ]

    if options[3] == 8 :
      options[3] = 'ALL'

    # Stores the name of the temporary key
    tempKey = ''

    # Creates a key using the user input
    for i in range( len(options) ) :
      tempKey = tempKey + str( options[i] )

      # Separates each element in the key by a hyphen
      if i != len(options) - 1 :
        tempKey = tempKey + '-' 

    # Reformats the key to be easier to read with the file names
    key = self.createKey( tempKey )

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

    # Initialize the mash tables for
    #   the maps and CSV files
    mapHash = self.initMapHash()
    csvHash = self.initCSVHash()

    # Check if there is a map for this dataset
    if mapHash.get( key ) != None :
      print( "map key: %s does exist" % key )
      fName = './static/maps/' + subName + '/' + mapHash[key]
    else :
      if csvHash.get( key ) == None :
        print( "csv key: %s doesn't exist" % key )
        
      # Creates a file path for where to store the cases CSV files
      csvPath = os.getcwd() + '/maptest/cases/'+ subName
      
      # Checks if a directory for the CSV data set exists
      # If not, then we create one
      if not os.path.isdir( csvPath ) :
        try :
          os.mkdir( csvPath )
        except OSError :
          print ("Command mkdir for directory %s has failed." % csvPath)
      else :
        print( 'this csv directory exists' )

      print( "map key: %s doesn't exist" % key )

      # Creates a file path for where to store the map html files
      mapPath = os.getcwd() + '/static/maps/'+ subName
    
      # Checks if a directory for the map data set exists
      # If not, then we create one
      if not os.path.isdir( mapPath ) :
        try :
          os.mkdir( mapPath )
        except OSError :
          print ("Command mkdir for directory %s has failed." % mapPath)

      fig = self.generateMap( subName, fName )

      # Add key and value to the HTML hash table 
      with open( './maptest/tables/html_table.txt', 'a' ) as fp :
        fp.write( key + ',' + fName + '.html\r\n' )

      fp.close()

    return key
#-------------------------------------------------------------



  # Takes a filename and generates the map requested by the user 
  def generateMap( self, dirName, fName ) :
    """
    TODO: Create a way to parse a folder from filename

    """
    path = ( './maptest/cases/'+ dirName + 
             '/' + fName + '.csv' )

    # Reads in the info from our COVID data set
    df = pd.read_csv(path, dtype={"FIPS": str}, encoding='UTF-8')

    # We manually insert the CommunityID column in the DataFrame
    #   object so it is compatible with the cholopleth parameter
    if fName[:3] != 'ALL' :
      # The color parameter in the choropleth function
      #   only takes in int data types
      df.loc[:,'CommunityID'] = int( fName[0] )

    # Creates the map object and fills it with 
    #   information
    fig = px.choropleth(df, geojson=counties, locations='FIPS', color='CommunityID',
                               # color_continuous_scale=px.colors.diverging.RdYlGn[::-1],
                               color_continuous_scale=px.colors.sequential.OrRd,
                               range_color=(1, 7),
                               scope="usa",
                               labels={'State':'State',
                                       'Area_Name':'County',
                                       'DensityPerSquaremileOfLandarea-Population':'Pop. Density per Square Mile of Land Area',
                                       'Median_Household_Income_2018':'Median Household Income in 2018',
                                       'Percent_of_adults_with_a_high_school_diploma_only_2014-18':'% Adults with High School Diplomas'}, 
                               hover_data=["Area_Name", "DensityPerSquaremileOfLandarea-Population", 
                                             "Median_Household_Income_2018", 
                                             "Percent_of_adults_with_a_high_school_diploma_only_2014-18"])

    # Fixes and displays the legend to the 
    #   right of the map
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      coloraxis_colorbar = dict(
                        title = dict( 
                          text = "Percentage Change in<br>the Number of New Cases",
                          font = dict(
                            size = 15)),
                        ticks = 'inside',
                        tickvals = [1, 2, 3, 4, 5, 6, 7],
                        ticktext = ['-100%: BIG DIP', '(-100%, 50%]: DOWNTICK', 
                                    '(-50%, 0%): DECREASE', '0%: FLAT',
                                    '(0%, 50%): INCREASE', '[50%, 100%): UPTICK', 
                                    'Greater than 100%: SPIKE'],
                        tickfont = dict(
                          size = 10),
                        thickness = 30,
                        xpad = 5,
                        len = 0.75))

    # Displays the figure when program is executed    
    #fig.show()
 
    # Path to the specific directory the file is stored in 
    nDir  = ( './static/maps/' + dirName + '/' )

    # Path to where to store the file for the hash table
    nFile = fName + '.html'

    # Creates an html file of the map
    pio.write_html(fig, file= nDir + nFile, auto_open=False)

    return fig
#-------------------------------------------------------------



  # Initializes the CSV Hash Table
  def initCSVHash( self ) :
    # The dictionary that stores all the keys to
    #   the csv file we want to generate maps from
    csvHash = {}

    # Empties out the file before we store new values
    open( './maptest/tables/csv_table.txt', 'w+' ).close()

    # Walks through each subdirectory in /cases/ and
    #   stores the names of the CSVs in csv_table.txt
    for path, subd, files in os.walk( './maptest/cases/' ) :
      for names in files:
        keys = names.replace( '.', '-' ).split( '-' )

        # Only the keys and CSV files will be stored 
        #   in csv_table.txt
        if keys[-1] == 'csv' :
          # Creates the key for each value in the
          #   CSV hash table
          key = ( keys[0] + '-' + keys[3] + 
                  '-' + keys[4] + '-' + keys[5][:2] +
                  '-' + keys[5][-2:] + '-' + keys[6] +
                  '-' + keys[7] + '-' + keys[-2][7:] )
          
          # Writes the values to csv_table.txt
          with open( './maptest/tables/csv_table.txt', 'a+' ) as fp :
            fp.write( key + ',' + names + '\r\n' )
          
          fp.close()

    with open( './maptest/tables/csv_table.txt', 'r' ) as fp :
      lines = fp.read().replace( '\r', '' ).split( '\n' )

    # Checks if the file is not empty
    if lines[0] != '' :
      for line in lines :
        line = line.split( ',' )

        key = line[0]

        # Indicates an end of file
        if key == '' :
          val = ''
        else :
          val = line[1]

        csvHash[key] = val
  
    return csvHash
#-------------------------------------------------------------



  # Initializes the Map Hash Table
  def initMapHash( self ) : 
    # The dictionary that stores all the keys to
    #   the html file we want to display to the
    #   home page iframe
    mapHash = {}

    with open( './maptest/tables/html_table.txt', 'r' ) as fp :
      lines = fp.read().replace( '\r', '' ).split( '\n' )

    fp.close()

    # Checks if the file is not empty
    if lines[0] != '' :
      for line in lines :
        line = line.split( ',' )

        key = line[0]

        # Indicates an end of file
        if key == '' :
          val = ''
        else :
          val = line[1]

        mapHash[key] = val
  
    return mapHash
#-------------------------------------------------------------



  # Formats the key of the hash table to be similar
  #   the names of all the .csv and .html files 
  def createKey( self, tempKey ) :
    key = ''
    front = ''
    middle = ''
    end = ''

    if( tempKey.endswith('ALL') ) :
      # Holds the ALL part of the string to be moved
      #   to the front of a key
      front = tempKey[-3:]

      if tempKey[1] == '-' :
        # Rearranges the string for key in order for
        #   it to fit the format of each files that
        #   will need to be read in
        middle = tempKey[1:-3]
        end    = tempKey[:1]
      else : 
        middle = tempKey[2:-3]
        end = tempKey[:2]
    else :
      # Otherwise, last element in the key will be 
      #   a single digit
      front = tempKey[-1:]

      if tempKey[1] == '-' :
        middle = tempKey[1:-1]
        end = tempKey[:1]
      else :
        middle = tempKey[2:-1]
        end = tempKey[:2]

    key = front + middle + end

    return key
#-------------------------------------------------------------

# This is how you'll call the class
# test = map_test( 7, '04-JUL-20', '04-AUG-20', 2 )
# test = map_test( 30, '04-JUL-20', '04-AUG-20', 8 )
# key = test.main()

