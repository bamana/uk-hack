# This script is used to query CDR using a given a domain name

import requests
import json
import os

if __name__ == '__main__' :
	
	# Read all domain names
	urls = open("all_domains.txt").read().splitlines()
	
	# Elasticsearch endpoint
	es_url = "https://els.istresearch.com:19200/memex-domains/weapons/_search"

	headers = {
		'Authorization': 'Basic bWVtZXg6cVJKZnUydVBrTUxtSDljcA==',
		'cache-control': 'no-cache',
		'postman-token': '12df510f-f3a3-5856-bbfb-8027ee79b13f',
		'Content-Type': 'application/json'
	}

	for url_curr in urls:

		query = "{\"query\":{\"filtered\":{\"filter\":{\"bool\":{\"must\":[{\"term\":{\"version\":\"2.0\"}},{\"term\":{\"url.domain\":{\"value\":\"" + url_curr + "\"}}},{\"term\":{\"content_type\":{\"value\":\"html\"}}}]}}}},\"size\":100,\"_source\":[\"id\", \"url\",\"raw_content\"]}"
		
		# Query elasticsearch
		response = requests.request("POST", es_url, headers=headers, data=query)

		output = json.loads(response.text)

		all_hits = output["hits"]

		if all_hits["total"] == 0 :
			continue

		hits = all_hits["hits"]

		os.mkdir("cdr_output/" + url_curr)

		for h in hits:
			out_file = open("cdr_output/" + url_curr + "/" + h["_id"] + ".html", "w")
			
			# These strings are unicode type
			url = h["_source"]["url"]
			content = h["_source"]["raw_content"]
			
			# Encode to 'UTF-8' and write to file
			out_file.write(content.encode('UTF-8'))

			out_file.close()

