import requests 
import datetime
import xtream
import json

import config

x = xtream

# Iris
x.server   = config.provider['server']
x.username = config.provider['username']
x.password = config.provider['password']

r = x.authenticate()

data = r.json()

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
  s = x.streams(x.liveType)
  live_stream_data = s.json() 
  # live_category_data is list of dict
  live_names = []
  live_IDs = []
  pos = 0
  while pos <= len(live_category_data) - 1:
    cat_streams_data = [item for item in live_stream_data if item['category_id'] == live_category_data[pos]['category_id']]
    live_names.append("{0:<30s} - {1:>3s} - {2:3d} streams".format(live_category_data[pos]['category_name'], live_category_data[pos]['category_id'], len(cat_streams_data)))
    total_streams += len(cat_streams_data)
    live_IDs.append(live_category_data[pos]['category_id'])
    pos += 1
  live_names.sort()

  if len(live_category_data) > 0:
    print 'Live Category Count:    {}\n[Name                          -  ID -  stream ct]'.format(len(live_category_data))
    print("==============================\n")

    for a,b in zip(live_names[::3],live_names[1::3]):
      print '{:<60}{:<}'.format(a,b)
    print("==============================\n")
except ValueError as err:
  print("Value error: {0}".format(err))

r = x.categories(x.vodType)

try:
  vod_category_data = r.json() 
  s = x.streams(x.vodType)
  vod_stream_data = s.json() 
  vod_names = []
  vod_IDs = []
  pos = 0
  while pos <= len(vod_category_data) - 1:
    cat_streams_data = [item for item in vod_stream_data if item['category_id'] == vod_category_data[pos]['category_id']]
    vod_names.append("{0:<30s} - {1:>3s} - {2:3d} streams".format(vod_category_data[pos]['category_name'], vod_category_data[pos]['category_id'], len(cat_streams_data)))
    total_streams += len(cat_streams_data)
    vod_IDs.append(vod_category_data[pos]['category_id'])
    pos += 1
  vod_names.sort()

  if len(vod_category_data) > 0:
    print 'VOD Category Count:     {}\n[Name                          -  ID -  stream ct]'.format(len(vod_category_data))
    print("==============================\n")

    for a,b in zip(vod_names[::3],vod_names[1::3]):
      print '{:<60}{:<}'.format(a,b)
    print("==============================\n")
except ValueError as err:
  print("Value error: {0}".format(err))

r = x.categories(x.seriesType)
try:
  series_category_data = r.json() 
  s = x.streams(x.seriesType)
  series_stream_data = s.json() 
  series_names = []
  series_IDs = []

  pos = 0
  while pos <= len(series_category_data) - 1:
    cat_streams_data = [item for item in series_stream_data if item['category_id'] == series_category_data[pos]['category_id']]
    series_names.append("{0:<30s} - {1:>3s} - {2:3d} streams".format(series_category_data[pos]['category_name'], series_category_data[pos]['category_id'], len(cat_streams_data)))
    total_streams += len(cat_streams_data)
    series_IDs.append(series_category_data[pos]['category_id'])
    pos += 1
  series_names.sort()

  if len(series_category_data) > 0:
    print 'Series Category Count:  {}\n[Name                          -  ID -  stream ct]'.format(len(series_category_data))
    print("==============================\n")

    for a,b in zip(series_names[::3],series_names[1::3]):
      print '{:<60}{:<}'.format(a,b)
    print("==============================\n")
except ValueError as err:
  print("Value error: {0}".format(err))

print 'Total Stream Count:     {}\n'.format(total_streams)

NoneType = type(None)

for i, entry in enumerate(live_category_data):
  print '\n\nStreams for Live category {} - {}:\n'.format(entry['category_id'],entry['category_name'])
  cat_streams_data = [item for item in live_stream_data if item['category_id'] == entry['category_id']]
  print "{0:<75s} {1:>5s} {2:>4s} ".format('name','ID', 'EPG?')
  for i, stream in enumerate(cat_streams_data):
    print "{0:<75s} {1:>5d} {2:>4d}".format(stream['name'].encode('utf-8'),stream['stream_id'],not isinstance(stream['epg_channel_id'], NoneType))

for i, entry in enumerate(vod_category_data):
  print '\n\nStreams for VOD category {} - {}:\n'.format(entry['category_id'],entry['category_name'])
  cat_streams_data = [item for item in vod_stream_data if item['category_id'] == entry['category_id']]
  print "{0:<75s} {1:>5s} {2:>4s} {3:>4s} ".format('name','ID','Type','Ext')
  for i, stream in enumerate(cat_streams_data):
# {u'direct_source': u'', u'rating': u'', u'added': u'1518032077', u'num': 1776, u'name': u'Linda Sweet Bare Love', u'stream_type': u'movie', u'stream_id': 17254, u'custom_sid': None, u'stream_icon': u'', u'container_extension': u'mp4', u'category_id': u'102', u'rating_5based': 0}
    print "{0:<75s} {1:>5d} {2:>4s} {3:>4s}".format(stream['name'].encode('utf-8'),stream['stream_id'],stream['stream_type'],stream['container_extension'])

for i, entry in enumerate(series_category_data):
  print '\n\nEpisodes for series category {} - {}:\n'.format(entry['category_id'],entry['category_name'])
  cat_streams_data = [item for item in series_stream_data if item['category_id'] == entry['category_id']]
  print "{0:<75s} {1:>5s} {2:>3s} {3:>3s} ".format('name','ID','S','E')
  for i, stream in enumerate(cat_streams_data):
    r = x.seriesInfoByID(stream['series_id'])
    series_info = r.json()
    season_count = len(series_info['episodes'])
    episode_count = 0
    for i, entry in enumerate(series_info['episodes']):
      episode_count += len(series_info['episodes'][str(entry)])
    print "{0:<75s} {1:>5d} {2:>3d} {3:>3d} ".format(stream['name'].encode('utf-8'),stream['series_id'],season_count,episode_count)
