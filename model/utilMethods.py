import threading
import geopy
import json
from config.dbconfig import pg_config
import psycopg2

# Definitions
NOMINATIM = 'nominatim'
GEONAMES = 'geonames'
MAPBOX = 'mapbox'
MAPQUEST = 'mapquest'
MAPTILER = 'maptiler'
OPENCAGE = 'opencage'
PHOTON = 'photon'
TOMTOM = 'tomtom'

geocoders = [
    NOMINATIM,
    GEONAMES,
    MAPBOX,
    MAPQUEST,
    MAPTILER,
    OPENCAGE,
    PHOTON,
    TOMTOM 
]

# Lat and Long constraints for PR
PR_TOP = 18.713150      # TOP, X    : lower
PR_RIGHT = -65.108251   # X, RIGHT  : lower
PR_BOT = 17.799704      # BOT, X    : higher
PR_LEFT = -68.057893    # X, LEFT   : higher

### HELPER FUNCTION ###

def locationByGeocoder(locator, address):
    try:
        location = locator.geocode(address)
    except:
        # Error locating given address
        return "ERROR"
    try: 
        res = str(location.latitude) + ',' + str(location.longitude)
        return res
    except:
        # Error extracting latitude and longitude attributes
        return "ERROR"
    
def geolocationConstraint(res):
    for k in res.keys():
        if res[k] == "ERROR":
            continue

        lat_lon = res[k].split(',') # [lon, lat]
        lat_lon[0] = float(lat_lon[0])
        lat_lon[1] = float(lat_lon[1])

        # Latitude and Longitude constraint
        if lat_lon[1] > PR_RIGHT or lat_lon[1] < PR_LEFT \
            or lat_lon[0] > PR_TOP or lat_lon[0] < PR_BOT:
            res[k] = "ERROR"

    return res


#######################

class utilMethodsDAO():
    
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % (pg_config['dbname'],
                                                                            pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)
    
    def addressToLatLon(self, address):
        res = {}
        threads = []
        for gc in geocoders:
            if gc == NOMINATIM:
                locator = geopy.Nominatim(user_agent="myGeocoder")
            elif gc == GEONAMES:
                locator = geopy.GeoNames('hmiranda8', user_agent="myGeocoder")
            elif gc == MAPBOX:
                api_key_MapBox = 'pk.eyJ1IjoiaG1pcmFuZGE4IiwiYSI6ImNsZnR5cTZ6cjA1bG8zZm1wcTFnZDVrOTYifQ.az5TI_e8ZD2rxcTw86Omyg'
                locator = geopy.MapBox(api_key=api_key_MapBox)
            elif gc == MAPQUEST:
                api_key_MapQuest = 'FIBdbLU94T0AiyCu9XoLs6VmDzHb26eg'
                locator = geopy.MapQuest(api_key=api_key_MapQuest)
            elif gc == MAPTILER:
                api_key_MapTiler = 'TyaOjQHGqd3N44bv1Jaj'
                locator = geopy.MapTiler(api_key=api_key_MapTiler)
            elif gc == OPENCAGE:
                api_key_OpenCage = 'd0fb0f34d05d4186a2f31293d1e369ba'
                locator = geopy.OpenCage(api_key=api_key_OpenCage)
            elif gc == PHOTON:
                locator = geopy.Photon()
            elif gc == TOMTOM:
                api_key_TomTom = 'XXKU3Qed8avLGuqMCGGSMWh1i35SvleZ'
                locator = geopy.TomTom(api_key=api_key_TomTom)
            
            # Create a new thread for each geocoder
            thread = threading.Thread(target=lambda: res.update({gc: locationByGeocoder(locator, address)}))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        res = geolocationConstraint(res)
        return res
    
    def monitor_outages(self):
        cursor = self.conn.cursor()
        query = "update outages_map set active = false where outage_date < current_date - interval '1 week'"
        cursor.execute(query)
        self.conn.commit()
        affected_rows = cursor.rowcount
        return affected_rows != 0