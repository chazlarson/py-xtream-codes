import requests
import datetime
import xtream
import json
import os

import config

def writeJSON(filename, data):
  if (config.write_files == 1):
    if not os.path.exists("data"):
      os.mkdir("data")
    with open("data/" + filename, 'w') as fp:
      json.dump(data, fp)

def EPGString(theNum):
  theString = "-"
  if (not isinstance(stream['epg_channel_id'], NoneType)):
    theString = stream['epg_channel_id']
  return theString

def VODName(json):
  try:
    return json['name']
  except KeyError:
    return 0

providername = config.provider['name']

x = xtream

# login details
x.server   = config.provider['server']
x.username = config.provider['username']
x.password = config.provider['password']

r = x.authenticate()

data = r.json()

writeJSON (providername + '-auth.json', data)

user_username = data['user_info']['username']
user_status = data['user_info']['status']
user_is_trial = data['user_info']['is_trial']
user_created_at = str(data['user_info']['created_at'])
if (user_created_at != 'None'):
  user_created_at = datetime.datetime.fromtimestamp(float(data['user_info']['created_at'].encode('ascii','ignore'))).isoformat()
user_auth = data['user_info']['auth']
user_allowed_output_formats = data['user_info']['allowed_output_formats']
user_exp_date = str(data['user_info']['exp_date'])
if (user_exp_date != 'None'):
  user_exp_date = datetime.datetime.fromtimestamp(float(data['user_info']['exp_date'].encode('ascii','ignore'))).isoformat()
user_active_cons = data['user_info']['active_cons']
user_message = data['user_info']['message']
user_password = data['user_info']['password']
user_max_connections = data['user_info']['max_connections']

server_https_port = data['server_info']['https_port']
server_url = data['server_info']['url']
server_time_now = data['server_info']['time_now']
server_server_protocol = data['server_info']['server_protocol']
server_timestamp_now = str(data['server_info']['timestamp_now'])
if (server_timestamp_now != 'None'):
  server_timestamp_now = datetime.datetime.fromtimestamp(float(data['server_info']['timestamp_now'])).isoformat()
server_timezone = data['server_info']['timezone']
server_rtmp_port = data['server_info']['rtmp_port']
server_port = data['server_info']['port']


# printing the output 
print("Account information:\n")

print 'Username:               {}'.format(user_username)
print 'Password:               {}'.format(user_password)
print 'Message:                {}'.format(user_message)
print 'Status:                 {}'.format(user_status)
print 'Authorized:             {}'.format(user_auth)
print 'Trial:                  {}'.format(user_is_trial)
print 'Created:                {}'.format(user_created_at)
print 'Expiration:             {}'.format(user_exp_date)
print 'Allowed output formats: {}'.format(user_allowed_output_formats)
print 'Max Connections:        {}'.format(user_max_connections)
print 'Active connections:     {}'.format(user_active_cons)
      
print("\nServer information:\n")

print 'Server address:         {}'.format(server_url)
print 'Protocol:               {}'.format(server_server_protocol)
print 'Port:                   {}'.format(server_port)
print 'HTTPS port:             {}'.format(server_https_port)
print 'RTMP port:              {}'.format(server_rtmp_port)
print 'Timezone:               {}'.format(server_timezone)
print 'Time now:               {}'.format(server_time_now)
print 'Timestamp now:          {}'.format(server_timestamp_now)

total_streams = 0

print("\n\nCategory information:\n")

r = x.categories(x.liveType)

try:
  live_category_data = r.json() 
  
  writeJSON (providername + '-live-categories.json', live_category_data)

  s = x.streams(x.liveType)
  live_stream_data = s.json() 

  writeJSON (providername + '-live-streams.json', live_stream_data)

  # live_category_data is list of dict
  live_names = []
  live_IDs = []
  pos = 0
  while pos <= len(live_category_data) - 1:
    cat_streams_data = [item for item in live_stream_data if item['category_id'] == live_category_data[pos]['category_id']]
    live_names.append("{0:<40s} - {1:>3s} - {2:4d} streams".format(live_category_data[pos]['category_name'], live_category_data[pos]['category_id'], len(cat_streams_data)))
    total_streams += len(cat_streams_data)
    live_IDs.append(live_category_data[pos]['category_id'])
    pos += 1
  live_names.sort()

  if len(live_category_data) > 0:
    print 'Live Category Count:                             {0:>4d}'.format(len(live_category_data))
    print("=====================================================")

    for i, entry in enumerate(live_names):
      print entry

    print("=====================================================\n")
except ValueError as err:
  print("Value error: {0}".format(err))

r = x.categories(x.vodType)

try:
  vod_category_data = r.json() 

  writeJSON (providername + '-vod-categories.json', vod_category_data)

  s = x.streams(x.vodType)
  vod_stream_data = s.json() 

  writeJSON (providername + '-vod-streams.json', vod_stream_data)

  vod_names = []
  vod_IDs = []
  pos = 0
  while pos <= len(vod_category_data) - 1:
    cat_streams_data = [item for item in vod_stream_data if item['category_id'] == vod_category_data[pos]['category_id']]
    vod_names.append("{0:<40s} - {1:>3s} - {2:4d} streams".format(vod_category_data[pos]['category_name'], vod_category_data[pos]['category_id'], len(cat_streams_data)))
    total_streams += len(cat_streams_data)
    vod_IDs.append(vod_category_data[pos]['category_id'])
    pos += 1
  vod_names.sort()

  if len(vod_category_data) > 0:
    print u'VOD Category Count:                              {0:>4d}'.format(len(vod_category_data))
    print("=====================================================")

    for i, entry in enumerate(vod_names):
      print entry

    print("=====================================================\n")
except ValueError as err:
  print("Value error: {0}".format(err))

r = x.categories(x.seriesType)
try:
  series_category_data = r.json() 

  writeJSON (providername + '-series-categories.json', series_category_data)

  s = x.streams(x.seriesType)
  series_stream_data = s.json() 

  writeJSON (providername + '-series-streams.json', series_stream_data)

  series_names = []
  series_IDs = []

  pos = 0
  while pos <= len(series_category_data) - 1:
    cat_streams_data = [item for item in series_stream_data if item['category_id'] == series_category_data[pos]['category_id']]
    writeJSON (series_category_data[pos]['category_id'] + '-stream-data.json', cat_streams_data)
    series_names.append(u"{0:<47s} - {1:>3s}".format(series_category_data[pos]['category_name'], series_category_data[pos]['category_id']))
    total_streams += len(cat_streams_data)
    series_IDs.append(series_category_data[pos]['category_id'])
    pos += 1
  series_names.sort()

  if len(series_category_data) > 0:
    print u'Series Category Count:                           {0:>4d}'.format(len(series_category_data))
    print("=====================================================")

    for i, entry in enumerate(series_names):
      print entry

    print("=====================================================\n")
except ValueError as err:
  print("Value error: {0}".format(err))

print 'Total Stream Count:     {}\n'.format(total_streams)

NoneType = type(None)

if (config.display_live_info == 1):
  live_category_data.sort(key=VODName)
  for i, entry in enumerate(live_category_data):
    print '\n\nStreams for Live category {} - {}:\n'.format(entry['category_id'],entry['category_name'])
    cat_streams_data = [item for item in live_stream_data if item['category_id'] == entry['category_id']]
    print u"{0:<75s} {1:>5s} {2:>4s} ".format('name','ID', 'EPG?')
    print u"======================================================================================"
    for i, stream in enumerate(cat_streams_data):
      print u"{0:<75s} {1:>5d} {2:>4s}".format(stream['name'],stream['stream_id'],EPGString(stream['epg_channel_id']))
    print u"======================================================================================"

if (config.display_vod_info == 1):
  for i, entry in enumerate(vod_category_data):
    print '\n\nStreams for VOD category {} - {}:\n'.format(entry['category_id'],entry['category_name'])
    cat_streams_data = [item for item in vod_stream_data if item['category_id'] == entry['category_id']]
    cat_streams_data.sort(key=VODName)
    print "{0:<75s} {1:>5s} {2:>5s} {3:>4s} {4:<6s} {5:<6s} {6:<9s} ".format('name','ID','Type','Ext','Video','Audio','W x H')
    print u"==================================================================================================================="
    for i, stream in enumerate(cat_streams_data):
  # {u'direct_source': u'', 
  #  u'rating': u'', 
  #  u'added': u'1518032077', 
  #  u'num': 1776, 
  #  u'name': u'Linda Sweet Bare Love', 
  #  u'stream_type': u'movie', 
  #  u'stream_id': 17254, 
  #  u'custom_sid': None, 
  #  u'stream_icon': u'', 
  #  u'container_extension': u'mp4', 
  #  u'category_id': u'102', 
  #  u'rating_5based': 0}
      r = x.vodInfoByID(stream['stream_id'])
      vod_stream_info = r.json()

      if (config.write_vod_info_files == 1):
        writeJSON (providername + '-vod-' + str(stream['stream_id']) + '-info.json', series_info)

      try:
        vcodec = vod_stream_info['info']['video']['codec_name']
        acodec = vod_stream_info['info']['audio']['codec_name']
        width = vod_stream_info['info']['video']['width']
        height = vod_stream_info['info']['video']['height']
      except TypeError:
        vcodec = u"none"
        acodec = u"none"
        width = 0
        height = 0
      except KeyError:
        vcodec = u"none"
        acodec = u"none"
        width = 0
        height = 0
      print u"{0:<75s} {1:>5d} {2:>5s} {3:>4s} {4:<6s} {5:<6s} {6:<4d}x{7:<4d} ".format(stream['name'],stream['stream_id'],stream['stream_type'],stream['container_extension'],vcodec,acodec,width,height)
    print u"==================================================================================================================="

if (config.display_series_info == 1):
  print u"{0:<60s} {1:>5s} {2:>3s} {3:>3s} ".format('name','ID','S','E')
  print u"=========================================================================="
  for i, entry in enumerate(series_category_data):
#     print '\n\nEpisodes for series category {} - {}:\n'.format(entry['category_id'],entry['category_name'])
    cat_streams_data = [item for item in series_stream_data if item['category_id'] == entry['category_id']]
    for i, stream in enumerate(cat_streams_data):
      r = x.seriesInfoByID(stream['series_id'])
      try:
        series_info = r.json()

        if (config.write_series_info_files == 1):
          writeJSON (providername + '-series-' + str(stream['series_id']) + '-info.json', series_info)

        season_count = len(series_info['episodes'])
        episode_count = 0
        for i, entry in enumerate(series_info['episodes']):
          episode_count += len(series_info['episodes'][str(entry)])
        print u"{0:<60s} {1:>5d} {2:>3d} {3:>3d} ".format(stream['name'],stream['series_id'],season_count,episode_count)
      except ValueError as err:
        print("Value error: {0} on series {0}".format(err, stream['series_id']))
  print u"=========================================================================="
