#!/usr/bin/env python3
import os
import json
import requests
from requests.auth import HTTPBasicAuth
import datetime
import time


def get_project(id):
    response = requests.get(
        url = api_url + "/projects/" + str(id) ,
        auth = HTTPBasicAuth(api_key, 'api_token') ,
        headers = {"Content-Type": "application/json"}
    )
    if not response.ok:
        raise Exception("ERROR: %s" % response.text)
    return response.text


def get_client(id):
    response = requests.get(
        url = api_url + "/clients/" + str(id) ,
        auth = HTTPBasicAuth(api_key, 'api_token') ,
        headers = {"Content-Type": "application/json"}
    )
    if not response.ok:
        raise Exception("ERROR: %s" % response.text)
    return response.text


def get_time_entries(date_start, date_end, date_offset):
    response = requests.get(
        url = api_url + "/time_entries" ,
        params = {
          "start_date": date_start.strftime('%Y-%m-%dT%H:%M:%S' + date_offset),
          "end_date"  : date_end.strftime('%Y-%m-%dT%H:%M:%S' + date_offset)
        } ,
        auth = HTTPBasicAuth(api_key, 'api_token') ,
        headers = {"Content-Type": "application/json"}
    )
    if not response.ok:
        sys.exit("ERROR: %s" % response.text)
    return response.text


api_url = "https://api.track.toggl.com/api/v8"
api_key = os.environ['TOGGL_API_KEY']
date_offset = "+03:00"
debug = False
date_start = datetime.datetime.now().date()
date_end = datetime.datetime.now().date() + datetime.timedelta(days=1)

time_entries = json.loads(get_time_entries(date_start, date_end, date_offset))
summary = []
for e in time_entries:
    pid = e.get('pid')
    if pid:
        project = json.loads(get_project(pid)).get('data')
    cid = project.get('cid')
    if cid:
      client = json.loads(get_client(cid)).get('data')
    #
    if debug:
      print("... entry")
      print(e)
      print("... project")
      print(project)
      print("... client")
      print(client)
    #
    cli = client.get('name')
    proj = project.get('name')
    desc = e.get('description')
    if desc is None: desc = ""
    seconds = e.get('duration')
    if seconds < 0: seconds = time.time()+seconds
    #
    summary.append({"client": cli, "project": proj, "description": desc, "duration": seconds})


for s in summary:
    print(
        "[%s] %s, %s - %s" %
        (
            s.get('client'),
            s.get('project'),
            s.get('description'),
            str(int(s.get('duration')/60))
        )
    )