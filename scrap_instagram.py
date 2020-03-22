import requests
import json
import urllib.parse
import logging
import sys

query_hash = "e769aa130647d2354c40ea6a439bfc08"
variable = json.loads("""
{"id":"30064447745","first":12}
""")
endpoint = "https://www.instagram.com/graphql/query/"

if sys.argv[1] != None:
    variable["id"] = sys.argv[1]

def constructParamters(queryhash, variable):
    return f"?query_hash={queryhash}&variables={urllib.parse.quote(json.dumps(variable))}"

def requestAPage(query_hash, variable):
    return requests.get(endpoint + constructParamters(query_hash, variable)).json()

def getContent(result):
    return list(map(lambda x: x["node"]["display_url"], result["data"]["user"]["edge_owner_to_timeline_media"]["edges"]))

fullList = []
while(True):
    result = requestAPage(query_hash, variable)
    pageInfo = result["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]
    nextCursor = pageInfo["end_cursor"]
    hasNextPage = pageInfo["has_next_page"]
    variable["after"] = nextCursor
    fullList += getContent(result)
    if not hasNextPage:
        break

for pic in fullList:
    print(pic)
