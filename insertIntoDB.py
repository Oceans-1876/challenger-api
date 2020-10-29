import pandas as pd
import psycopg2
import os
from sqlalchemy import create_engine
#import ppygis
from geoalchemy2 import Geometry
import math


rootPath = "/home/mwiecksosa/oceans1876/"
dataPath = rootPath+"data/"



def main():
    engine = create_engine('postgresql://postgres:pw123@localhost:5432/oceans-1876')

    param_dic = {
        "host"      : "localhost",
        "database"  : "oceans-1876",
        "user"      : "postgres",
        "password"  : "pw123"
    }

    dfToPSQL_list = ["Station.csv","Meta.csv","Species.csv","Image.csv",
                     "AirCondition.csv","WaterCondition.csv"]
    saveName_df_stationLines = dataPath+"stationLines_allStations.csv"
    saveName_df_verifiedSpeciesNames = dataPath+"verifiedSpeciesNames_allStations.csv"
    saveName_df_stationEnvironmentInfo = dataPath+"stationEnvironmentInfo_allStations.csv"
    df_stationLines = pd.read_csv(saveName_df_stationLines)
    df_verifiedSpeciesNames = pd.read_csv(saveName_df_verifiedSpeciesNames)
    df_stationEnvironmentInfo = pd.read_csv(saveName_df_stationEnvironmentInfo)


    insertStations(df_stationLines,df_verifiedSpeciesNames,df_stationEnvironmentInfo,engine,param_dic)

    insertSpecies(df_stationLines,df_verifiedSpeciesNames,df_stationEnvironmentInfo,engine,param_dic)

    insertSpeciesStations(df_stationLines,df_verifiedSpeciesNames,df_stationEnvironmentInfo,engine,param_dic)

    insertAirCondition(df_stationLines,df_verifiedSpeciesNames,df_stationEnvironmentInfo,engine,param_dic)

    insertImage(df_stationLines,df_verifiedSpeciesNames,df_stationEnvironmentInfo,engine,param_dic)

    insertMeta(df_stationLines,df_verifiedSpeciesNames,df_stationEnvironmentInfo,engine,param_dic)

    insertWaterCondition(df_stationLines,df_verifiedSpeciesNames,df_stationEnvironmentInfo,engine,param_dic)


def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    return conn


def single_insert(conn, insert_req):
    """ Execute a single INSERT request """
    cursor = conn.cursor()
    try:
        cursor.execute(insert_req)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    cursor.close()




def insertStations(df_stationLines,df_verifiedSpeciesNames,df_stationEnvironmentInfo,engine,param_dic):

    ###### input stations ######

    index = list(range(len(df_stationEnvironmentInfo)))

    # id
    id = list(range(len(df_stationEnvironmentInfo)))

    # meta
        # don't have this

    # station
    station = df_stationEnvironmentInfo['currentStation']

    # location_name
        # don't have this
    # location_original_text
        # don't have this

    # location_point
    # (lat,long) is (y,x)
    #location_point = [(long,lat) for lat,long in zip(df_stationEnvironmentInfo['currentLatCoord'],\
    #                                                 df_stationEnvironmentInfo['currentLongCoord'])]

    # species
        # using backref

    # water_conditions
        # using backref

    # air_conditions
        # using backref

    # images
        # using backref

    # station_text_start_line
    # getting mismatching station numbers.. fix later
    # station_text_start_line = df_stationLines['startLine']

    # station_text_end_line
    # getting mismatching station numbers.. fix later
    #station_text_end_line = df_stationLines['endLine']

    #stationsData = [id,station,location_point]
    #for list in stationsData:
    #    print(len(list))
    #listOfColnames = ["id","station","location_point"]

    location_name = ["NA"]*len(id)
    location_original_text = ["NA"]*len(id)
    station_text_start_line = ["NA"]*len(id)
    station_text_end_line = ["NA"]*len(id)

    stationsDF = pd.DataFrame({"id":id,
                               "station":station,
                               "location_name":location_name,
                               "location_original_text":location_original_text,
                               #"location_point":location_point,
                               "station_text_start_line":station_text_start_line,
                               "station_text_end_line":station_text_end_line})

    longList = []
    for long in df_stationEnvironmentInfo['currentLongCoord']:
        #print(long)
        if math.isnan(long):
            longList.append("0")
        else:
            longList.append(long)
    df_stationEnvironmentInfo['currentLongCoord'] = longList
    latList = []
    for lat in df_stationEnvironmentInfo['currentLatCoord']:
        if math.isnan(lat):
            latList.append("0")
        else:
            latList.append(lat)
    df_stationEnvironmentInfo['currentLatCoord'] = latList

    stationsDF['location_point'] = "POINT(" + df_stationEnvironmentInfo['currentLongCoord'].astype(str) + " " + df_stationEnvironmentInfo['currentLatCoord'].astype(str) + ")"

    #https://gis.stackexchange.com/questions/336220/dataframe-of-points-to-postgis
    #how to do the geometry point ....

    #columnsToKeep = ["id","station","location_name","location_original_text","location_point","station_text_start_line","station_text_end_line"]
    #stationsDF = stationsDF[columnsToKeep]
    stationsDF.to_sql('station', engine, dtype={'location_point': Geometry(geometry_type='POINT', srid=4326)}, if_exists='append', index=False, chunksize=1000)
    #csv_data_frame.to_sql(table_name, engine, if_exists='append', index=False, chunksize=1000)

    #  id | station | location_name | location_original_text | location_point | station_text_start_line | station_text_end_line


    """
    # Connecting to the database
    connection = connect(param_dic)
    cursor = connection.cursor()



    #c.execute('''INSERT INTO tweets(tweet_id, created_date, text, screen_name, geom) VALUES (%s,%s,%s,%s,ST_GeomFromText(%s,4326))''', (long(tweet.id), tweet_date, tweet_text, user, coordinates))

    # Inserting each row
    for i in stationsDF.index:

        coordinates = "POINT(%s,%s)" % (stationsDF.loc[i,"location_point"][0],stationsDF.loc[i,"location_point"][1])

        ###query = ### INSERT into station(id, station, location_name, location_original_text, location_point, station_text_start_line, station_text_end_line) VALUES (%s,"%s",%s,%s,ST_GeomFromText(%s),%s,%s);###\
        ###% (stationsDF.loc[i,"id"], stationsDF.loc[i,"station"], stationsDF.loc[i,"location_name"],
        ###    stationsDF.loc[i,"location_original_text"],coordinates,
        ###    stationsDF.loc[i,"station_text_start_line"],stationsDF.loc[i,"station_text_end_line"])


        ###print("query",query)

        cursor.execute('''INSERT into station VALUES (%s,%s,%s,%s,ST_GeomFromText(%s),%s,%s)''',(stationsDF.loc[i,"id"],stationsDF.loc[i,"station"],stationsDF.loc[i,"location_name"],stationsDF.loc[i,"location_original_text"],coordinates,stationsDF.loc[i,"station_text_start_line"],stationsDF.loc[i,"station_text_end_line"]))

        ###use cursor isntead of insert...
        ####single_insert(conn, query)


    #conn.commit()  # save data

    # Close the connection
    conn.close()

    #  id | station | location_name | location_original_text | location_point | station_text_start_line | station_text_end_line
    # do we even need this?

    """



def insertSpeciesStations(df_stationLines,df_verifiedSpeciesNames,df_stationEnvironmentInfo,engine,param_dic):

    """
    species_stations = db.Table(
        "species_stations",
        db.Column("species_id", db.Integer, db.ForeignKey("species.id"), primary_key=True),
        db.Column("station_id", db.Integer, db.ForeignKey("station.id"), primary_key=True),
        db.Column("date", db.Date),
        db.Column("count", db.Integer),
        db.Column("notes", db.Text),
    )
    """

    species_id = list(range(len(df_verifiedSpeciesNames)))
    ########## WILL NEED TO FIX LATER #################
    # this is definitely going to mess something up alter because the station IDs
    # do not match across the different CSVs

    unqStations = df_verifiedSpeciesNames.station.unique()
    idsToDistribute = list(range(len(df_verifiedSpeciesNames.station.unique())))
    station_id = []

    for stn in df_verifiedSpeciesNames['station']:
        for i in range(len(unqStations)):
            if stn == unqStations[i]:
                station_id.append(idsToDistribute[i])




    #date = df_stationEnvironmentInfo['currentDate']
    unqStations = df_verifiedSpeciesNames.station.unique()

    date = ["NA"]*len(station_id)
    #date = []
    #for i,row in df_verifiedSpeciesNames.iterrows():
    #    for j,row2 in df_stationEnvironmentInfo.iterrows():
    #        if row.station == row2.currentStation:
    #            date.append(row2.currentDate)


    count = ["NA"]*len(station_id)

    notes = ["NA"]*len(station_id)

    species_stationsDF = pd.DataFrame({"species_id":species_id,
                                       "station_id":station_id,
                                       "date":date,
                                       "count":count,
                                       "notes":notes})

    #imageDF.to_sql('image', engine, if_exists='append', index=False, chunksize=1000)
    species_stationsDF.to_sql('species_stations', engine, if_exists='append', index=False, chunksize=1000)

    """
    conn = connect(param_dic)

    # Inserting each row
    for i in species_stationsDF.index:

        query = ### INSERT into species_stations(species_id, station_id, date, count, notes) VALUES (%s,%s,%s,%s,%s); ###\
         % (species_stationsDF.loc[i,"species_id"], species_stationsDF.loc[i,"station_id"],
            species_stationsDF.loc[i,"date"], species_stationsDF.loc[i,"count"],
            species_stationsDF.loc[i,"notes"])


        single_insert(conn, query)

        #  species_id | station_id | date | count | notes

    # Close the connection
    conn.close()
    """


def insertSpecies(df_stationLines,df_verifiedSpeciesNames,df_stationEnvironmentInfo,engine,param_dic):

    id = list(range(len(df_verifiedSpeciesNames)))
    common_name = df_verifiedSpeciesNames['vernacular']
    scientific_name = df_verifiedSpeciesNames['canonicalForm']
    original_name = df_verifiedSpeciesNames['speciesName']
    verified = df_verifiedSpeciesNames['verified']
    classification_path = df_verifiedSpeciesNames['classificationPath']
    classification_path_rank = df_verifiedSpeciesNames['classificationPathRank']
    data_source = df_verifiedSpeciesNames['dataSource']
    gni_UUID = df_verifiedSpeciesNames['gniUUID']


    speciesDF = pd.DataFrame({"id":id,
                              "common_name":common_name,
                              "scientific_name":scientific_name,
                              "original_name":original_name,
                              "classification_path":classification_path,
                              "classification_path_rank":classification_path_rank,
                              "data_source":data_source,
                              "gni_UUID":gni_UUID})
    speciesDF.to_sql('species', engine, if_exists='append', index=False, chunksize=1000)

    """
    conn = connect(param_dic)

    # Inserting each row
    for i in speciesDF.index:

        query = ###
        INSERT into species(id, common_name, scientific_name, original_name, classification_path, classification_path_rank, data_source, gni_UUID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);### \
        % (speciesDF.loc[i,"id"], speciesDF.loc[i,"common_name"], speciesDF.loc[i,"scientific_name"],
            speciesDF.loc[i,"original_name"], speciesDF.loc[i,"classification_path"],
            speciesDF.loc[i,"classification_path_rank"], speciesDF.loc[i,"data_source"],
            speciesDF.loc[i,"gni_UUID"])


        single_insert(conn, query)

    # Close the connection
    conn.close()

    """
# index	Unnamed: 0	Unnamed: 0.1	station	speciesName	offsetStart	offsetEnd	vernacular	canonicalForm	verified	dataSource	gniUUID	classificationPath	classificationPathRank


def insertMeta(df_stationLines,df_verifiedSpeciesNames,df_stationEnvironmentInfo,engine,param_dic):
    id = list(range(len(df_stationEnvironmentInfo)))
    station_id =list(range(len(df_stationEnvironmentInfo)))
    pages = ["NA"]*len(id)

    metaDF = pd.DataFrame({"id":id,
                           "station_id":station_id,
                           "pages":pages})
    metaDF.to_sql('meta', engine, if_exists='append', index=False, chunksize=1000)

    """
    conn = connect(param_dic)

    # Inserting each row
    for i in metaDF.index:

        query = ###INSERT into meta(id, station_id, date) VALUES (%s,%s,%s);###\
         % (metaDF.loc[i,"id"], metaDF.loc[i,"station_id"], metaDF.loc[i,"date"])


        single_insert(conn, query)

    # Close the connection
    conn.close()
    """


def insertImage(df_stationLines,df_verifiedSpeciesNames,df_stationEnvironmentInfo,engine,param_dic):
    id = list(range(len(df_stationEnvironmentInfo)))
    station_id = list(range(len(df_stationEnvironmentInfo)))
    date = df_stationEnvironmentInfo['currentDate']

    imageDF = pd.DataFrame({"id":id,
                            "station_id":station_id,
                            "date":date})
    imageDF.to_sql('image', engine, if_exists='append', index=False, chunksize=1000)

    """
    conn = connect(param_dic)

    # Inserting each row
    for i in imageDF.index:

        query = ### INSERT into image(id, station_id, date) VALUES (%s,%s,%s);###\
         % (imageDF.loc[i,"id"], imageDF.loc[i,"station_id"], imageDF.loc[i,"date"])


        single_insert(conn, query)

    # Close the connection
    conn.close()
    """


def insertWaterCondition(df_stationLines,df_verifiedSpeciesNames,df_stationEnvironmentInfo,engine,param_dic):

    id = list(range(len(df_stationEnvironmentInfo)))

    station = df_stationEnvironmentInfo['currentStation']
    station_id = list(range(len(df_stationEnvironmentInfo)))
    #fix later to use backref correctly
    #station = db.relationship("Station", backref="station", lazy=True, uselist=False)
    #station_id = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)

    date = df_stationEnvironmentInfo['currentDate']
    water_temp_surace = df_stationEnvironmentInfo['currentWaterTempSurfaceDegree']
    water_temp_bottom = df_stationEnvironmentInfo['currentWaterTempBottomDegree']
    water_density_surace_60F = df_stationEnvironmentInfo['currentWaterDensitySurfaceNumber']
    water_density_bottom_60F = df_stationEnvironmentInfo['currentWaterDensityBottomNumber']

    waterConditionsDF = pd.DataFrame({"id":id,
                              "station_id":station_id,
                              "date":date,"water_temp_surace":water_temp_surace,
                              "water_temp_bottom":water_temp_bottom,
                              "water_density_surace_60F":water_density_surace_60F,
                              "water_density_bottom_60F":water_density_bottom_60F})

    waterConditionsDF.to_sql('water_condition', engine, if_exists='append', index=False, chunksize=1000)


    """
    conn = connect(param_dic)

    # Inserting each row
    for i in waterConditionsDF.index:

        query = ###INSERT into water_condition(id, station_id, date, water_temp_surace, water_temp_bottom, water_density_surace_60F, water_density_bottom_60F) VALUES (%s,%s,%s,%s,%s,%s,%s);###\
         % (waterConditionsDF.loc[i,"id"], waterConditionsDF.loc[i,"station_id"], waterConditionsDF.loc[i,"date"],
            waterConditionsDF.loc[i,"water_temp_surace"],waterConditionsDF.loc[i,"water_temp_bottom"],
            waterConditionsDF.loc[i,"water_density_surace_60F"], waterConditionsDF.loc[i,"water_density_bottom_60F"])

        single_insert(conn, query)

    # Close the connection
    conn.close()


    #  id | station_id | date | water_temp_surace | water_temp_bottom | water_density_surace_60F | water_density_bottom_60F

    #waterConditionsDF.to_sql('waterConditions', engine, if_exists='append', index=False, chunksize=1000)
#index	Unnamed: 0	currentStation	currentDate	currentDMSCoords	currentLatDegree	currentLatMinute	currentLatSecond	currentLatCoord	currentLongDegree	currentLongMinute	currentLongSecond	currentLongCoord	currentAirTempNoon	currentAirTempNoonDegree	currentAirTempDailyMean	currentAirTempDailyMeanDegree	currentWaterTempSurface	currentWaterTempSurfaceDegree	currentWaterTempBottom	currentWaterTempBottomDegree	currentWaterDensitySurface	currentWaterDensitySurfaceNumber	currentWaterDensityBottom	currentWaterDensityBottomNumber	lineNumberOfDate	lineNumberOfLatLong	lineNumberAirTempNoon	lineNumberOfAirTempDailyMean	lineNumberOfWaterTempSurface	lineNumberOfWaterTempBottom	lineNumberOfWaterDensitySurface	lineNumberOfWaterDensityBottom

    """


def insertAirCondition(df_stationLines,df_verifiedSpeciesNames,df_stationEnvironmentInfo,engine,param_dic):

    id = list(range(len(df_stationEnvironmentInfo)))
    station = df_stationEnvironmentInfo['currentStation']
    station_id = list(range(len(df_stationEnvironmentInfo)))
    #fix later to use backref correctly
    #station = db.relationship("Station", backref="station", lazy=True, uselist=False)
    #station_id = db.Column(db.Integer, db.ForeignKey("station.id"), nullable=False)

    date = df_stationEnvironmentInfo['currentDate']

    air_temp_noon = df_stationEnvironmentInfo['currentAirTempNoonDegree']
    air_temp_daily_mean = df_stationEnvironmentInfo['currentAirTempDailyMeanDegree']

    airConditionsDF = pd.DataFrame({"id":id,
                                    "station_id":station_id,
                                    "date":date,
                                    "air_temp_noon":air_temp_noon,
                                    "air_temp_daily_mean":air_temp_daily_mean})


    airConditionsDF.to_sql('air_condition', engine, if_exists='append', index=False, chunksize=1000)

    """
    conn = connect(param_dic)

    # Inserting each row
    for i in airConditionsDF.index:

        query = ###INSERT into air_condition(id, station_id, date, air_temp_noon, air_temp_daily_mean) VALUES (%s,%s,%s,%s,%s);###\
         % (airConditionsDF.loc[i,"id"], airConditionsDF.loc[i,"station_id"], airConditionsDF.loc[i,"date"],
            airConditionsDF.loc[i,"air_temp_noon"], airConditionsDF.loc[i,"air_temp_daily_mean"])

        single_insert(conn, query)

    # Close the connection
    conn.close()

    #  id | station_id | date | air_temp_noon | air_temp_daily_mean

    """

=
if __name__ == '__main__':
    main()
