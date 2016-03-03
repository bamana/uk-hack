__Author___='Yuhao Zhu'

import httplib, urllib
import json
import requests
import os

def get_domain_name(raw_domain_name):
    if raw_domain_name[:4] == "www.":
        return raw_domain_name[4:]
    return raw_domain_name

def post(domain_name):
    params = {"query":{"filtered":{"filter":{"bool":{"must":[{"term":{"version":"2.0"}},{"term":{"url.domain":{"value":domain_name}}},{"term":{"content_type":{"value":"html"}}}]}}}},"size":105}
    headers = {"Content-type": "application/json",
            "Authorization": "Basic bWVtZXg6cVJKZnUydVBrTUxtSDljcA=="}
    url = "https://els.istresearch.com:19200/memex-domains/weapons/_search"
    r = requests.post(url,data=json.dumps(params),headers=headers)
    return r.json()

def process(doc,success,domain):
    #jsonStr = json.dumps(doc)
    #doc=json.loads(jsonStr)
    hits_total= int(doc["hits"]["total"])
    if hits_total >= 105:
        print "\t"+"We have "+str(hits_total)+ ", which is enough!"
        success=success+1
    else:
        print "\t"+"We only have " + str(hits_total)+ "\tWe need to manually download more..."
    hits=doc["hits"]["hits"]
    if not os.path.exists(os.getcwd()+"/data/"+domain):
        os.makedirs(os.getcwd()+"/data/"+domain)
    if not os.path.exists(os.getcwd()+"/data/"+domain+"/training"):
        os.makedirs(os.getcwd()+"/data/"+domain+"/training")
    if not os.path.exists(os.getcwd()+"/data/"+domain+"/test"):
        os.makedirs(os.getcwd()+"/data/"+domain+"/test")
    for hit in hits:
        filename=hit["_id"]+".html"
        content=hit["_source"]["raw_content"]
        content=content.encode('utf-8')
#        content=content.replace('\x0D','')
        url = hit["_source"]["url"]
        with open(os.getcwd()+"/data/"+domain+"/test/"+filename,'w') as f:
            f.write(content)
        with open(domain+"_urls",'a') as f:
            f.write(filename+"\t"+url+'\n')
    return success
    
domain_name=["apps.nevadaappeal.com","www.abqjournal.com","www.alaskaslist.com","www.billingsthriftynickel.com",
"www.carolinabargaintrader.net","www.carolinabargaintrader.net","www.clasificadosphoenix.univision.com","www.classifiednc.com",
"www.classifieds.al.com","www.cologunmarket.com","www.comprayventadearms.com","www.dallasguns.com","www.elpasoguntrader.com",
"www.fhclassifieds.com","www.floridagunclassifieds.com","www.floridaguntrader.com","www.gowilkes.com","www.gunidaho.com","www.hawaiiguntrader.com","www.idahogunsforsale.com","www.iguntrade.com","www.jasonsguns.com","www.ksl.com","www.kyclassifieds.com","www.midutahradio.com/tradio","www.midwestgtrader.com","www.montanagunclassifieds.com","www.montanagunsforsale.com","www.mountaintrader.com","www.msguntrader.com","www.ncgunads.com","www.ncgunads.com","www.nextechclassifieds.com","www.sanjoseguntrader.com","www.tell-n-sell.com","www.tennesseegunexchange.com","www.theoutdoorstrader.com","www.tradesnsales.com","www.upstateguntrader.com","www.vci-classifieds.com","www.zidaho.com"]
success=0
for name in domain_name:
    print "Sending POST request for "+name
    doc=post(get_domain_name(name))
    success=process(doc,success,name)

print "Success: "+str(success)+ " of " + str(len(domain_name)) 
