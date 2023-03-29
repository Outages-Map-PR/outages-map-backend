import geopy

class utilMethodsDAO():
    
    def addressToLatLon(self, address):
        actual = address['address']
        locator = geopy.Nominatim(user_agent="myGeocoder")
        location = locator.geocode(actual)
        try:
            lat = location.latitude 
            lon = location.longitude
            return (lat, lon)
        except:
            return "error"
        