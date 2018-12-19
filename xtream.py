import requests 
import datetime

server = "http://foo.bar:666"
username = "ernie"
password = "bert"

liveType = "Live"
vodType = "VOD"
seriesType = "Series"

class XCCache:
    authData = {}

cc = XCCache()    
# Note: The API Does not provide Full links to the requested stream. You have to build the url to the stream in order to play it.
# 
# For Live Streams the main format is
#            http(s)://domain:port/live/username/password/streamID.ext ( In  allowed_output_formats element you have the available ext )
# 
# For VOD Streams the format is:
# 
# http(s)://domain:port/movie/username/password/streamID.ext ( In  target_container element you have the available ext )
#  
# For Series Streams the format is
# 
# http(s)://domain:port/series/username/password/streamID.ext ( In  target_container element you have the available ext )


# If you want to limit the displayed output data, you can use params[offset]=X & params[items_per_page]=X on your call.

# Authentication returns information about the account and server:
def authenticate():
    r = requests.get(get_authenticate_URL())
    cc.authData = r.json()
    return r

# GET Stream Categories
def categories(streamType):
    theURL = ""
    if streamType == liveType:
        theURL = get_live_categories_URL()
    elif streamType == vodType:
        theURL = get_vod_cat_URL()
    elif streamType == seriesType:
        theURL = get_series_cat_URL()
    else:
        theURL = ""

    r = requests.get(theURL)
    return r

# GET Streams
def streams(streamType):
    theURL = ""
    if streamType == liveType:
        theURL = get_live_streams_URL()
    elif streamType == vodType:
        theURL = get_vod_streams_URL()
    elif streamType == seriesType:
        theURL = get_series_URL()
    else:
        theURL = ""

    r = requests.get(theURL) 
    return r

# GET Streams by Category
def streamsByCategory(streamType, category_id):
    theURL = ""
    if streamType == liveType:
        theURL = get_live_streams_URL_by_category(category_id)
    elif streamType == vodType:
        theURL = get_vod_streams_URL_by_category(category_id)
    elif streamType == seriesType:
        theURL = get_series_URL_by_category(category_id)
    else:
        theURL = ""

    r = requests.get(theURL) 
    return r

# GET SERIES Info
def seriesInfoByID(series_id):  
    r = requests.get(get_series_info_URL_by_ID(series_id)) 
    return r
# The seasons array, might be filled or might be completely empty. 
# If it is not empty, it will contain the cover, overview and the air date of the selected season.
# In your APP if you want to display the series, you have to take that from the episodes array.

# GET VOD Info
def vodInfoByID(vod_id):  
    r = requests.get(get_VOD_info_URL_by_ID(vod_id)) 
    return r

# GET short_epg for LIVE Streams (same as stalker portal, prints the next X EPG that will play soon)
def liveEpgByStream(stream_id):  
    r = requests.get(get_live_epg_URL_by_stream(stream_id)) 
    return r

def liveEpgByStreamAndLimit(stream_id, limit):  
    r = requests.get(get_live_epg_URL_by_stream_and_limit(stream_id, limit)) 
    return r

#  GET ALL EPG for LIVE Streams (same as stalker portal, but it will print all epg listings regardless of the day)
def allLiveEpgByStream(stream_id):  
    r = requests.get(get_all_live_epg_URL_by_stream(stream_id)) 
    return r

# Full EPG List for all Streams
def allEpg():  
    r = requests.get(get_all_epg_URL()) 
    return r


## URL-builder methods

def get_authenticate_URL():  
    URL = '%s/player_api.php?username=%s&password=%s' % (server, username, password) 
    return URL

def get_live_categories_URL():  
    URL = '%s/player_api.php?username=%s&password=%s&action=%s' % (server, username, password, 'get_live_categories')  
    return URL

def get_live_streams_URL():  
    URL = '%s/player_api.php?username=%s&password=%s&action=%s' % (server, username, password, 'get_live_streams')  
    return URL

def get_live_streams_URL_by_category(category_id):  
    URL = '%s/player_api.php?username=%s&password=%s&action=%s&category_id=%s' % (server, username, password, 'get_live_streams', category_id)
    return URL

def get_vod_cat_URL():  
    URL = '%s/player_api.php?username=%s&password=%s&action=%s' % (server, username, password, 'get_vod_categories')  
    return URL

def get_vod_streams_URL():  
    URL = '%s/player_api.php?username=%s&password=%s&action=%s' % (server, username, password, 'get_vod_streams')  
    return URL

def get_vod_streams_URL_by_category(category_id):  
    URL = '%s/player_api.php?username=%s&password=%s&action=%s&category_id=%s' % (server, username, password, 'get_vod_streams', category_id)
    return URL

def get_series_cat_URL():  
    URL = '%s/player_api.php?username=%s&password=%s&action=%s' % (server, username, password, 'get_series_categories')  
    return URL

def get_series_URL():  
    URL = '%s/player_api.php?username=%s&password=%s&action=%s' % (server, username, password, 'get_series')  
    return URL

def get_series_URL_by_category(category_id):  
    URL = '%s/player_api.php?username=%s&password=%s&action=%s&category_id=%s' % (server, username, password, 'get_series', category_id)  
    return URL

def get_series_info_URL_by_ID(series_id):  
    URL = '%s/player_api.php?username=%s&password=%s&action=%s&series_id=%s' % (server, username, password, 'get_series_info', series_id)  
    return URL

def get_VOD_info_URL_by_ID(vod_id):  
    URL = '%s/player_api.php?username=%s&password=%s&action=%s&vod_id=%s' % (server, username, password, 'get_vod_info', vod_id)  
    return URL

def get_live_epg_URL_by_stream(stream_id):  
    URL = '%s/player_api.php?username=%s&password=%s&action=%s&stream_id=%s' % (server, username, password, 'get_short_epg', stream_id)  
    return URL

def get_live_epg_URL_by_stream_and_limit(stream_id, limit):  
    URL = '%s/player_api.php?username=%s&password=%s&action=%s&stream_id=%s&limit=%s' % (server, username, password, 'get_short_epg', stream_id, limit)  
    return URL

def get_all_live_epg_URL_by_stream(stream_id):  
    URL = '%s/player_api.php?username=%s&password=%s&action=%s&stream_id=%s' % (server, username, password, 'get_simple_data_table', stream_id)  
    return URL

def get_all_epg_URL():  
    URL = '%s/xmltv.php?username=%s&password=%s' % (server, username, password)  
    return URL
