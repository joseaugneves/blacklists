from typing import Union
from fastapi import FastAPI, Body,Request,Header
from pydantic import BaseModel
from pprint import pprint
import blacklist as black
from fastapivars import fastapi_vars
from typing_extensions import TypedDict
import enum
from fastapi.responses import PlainTextResponse
import datetime

app = FastAPI()

class Item(BaseModel):
    item_id: int
    item_name: str

class JsonFormatG(TypedDict):
    urllist: list[str]

class JsonFormatD(TypedDict):
    dictionary: dict

# class TestQuery(enum.Enum):
#     Tenable= "Tenable"
#     Shodan = "shodan"
#     #Qualys ="qualys"
#     Censys ="censys"

class ops(enum.Enum) :
    all="all"
    noipv6="ipv4"
    noipv4="ipv6"
    
def parce (data,ops:str):
    lines=data.split('\r\n')
    ipv4_list = []
    ipv6_list = []
    data0=""
    for ip in lines:
        if "." in ip:
            ipv4_list.append(ip)
        else:
            ipv6_list.append(ip)
    if ops =='ipv6':data0="\r\n".join(ipv6_list)
    if ops =='ipv4':data0="\r\n".join(ipv4_list)
    return data0

loggd=[{'date':"",'ip':"127.0.0.1",'event':'init'}]
loggl=[]
loggl.append(loggd)

def logge(mess,hostt):
    vars=fastapi_vars
    l={'date':f'{datetime.datetime.now()}','ip':hostt,'event':mess}
    loggl=vars.getvar('log')
    print ("reeded :",loggl)
    loggl.append(l)
    print ("appended :",loggl)
    vars.addvar('log',loggl)
    return

@app.on_event('startup')
def init_data():
    vars=fastapi_vars
    vars.addvar('log',loggd)


@app.get("/log",summary="see log iteractions")
def log() :
    vars=fastapi_vars
    log=vars.getvar('log')
    print ("logfile")
    pprint(f"{log}")
    return (log)

@app.get("/misp/{days}",summary="retrive n days Misp atackers ip's",response_class=PlainTextResponse)
def get_attackers(days: int,request: Request):
    client_host = request.client.host
    logge(f'misp/{days}',client_host)
    return (black.misp(days))

@app.get("/allbacklist_text/{days}",summary="generate all list contents in fw format with misp",description=" see lists on allblackllist_dict",response_class=PlainTextResponse)
def read_allblack_text(days:int,request: Request,choice: ops):
    client_host = request.client.host
    logge("allblacklists",client_host)
    black.getdb()
    print(black.db.values())
    urllist=list(black.db.values())
    ips=black.parceip(urllist)
    flatt= [item for sublist in ips for item in sublist]
    #ips = "\n\n".join(flattened)
    ipsrct=list(set(flatt))
    data2="\r\n".join(ipsrct)
    data3=black.misp(days)
    #data3=""
    dat=data2+"\r\n"+data3
    print (choice.value,type(choice),"\r\n"+dat)
    if choice.value.__contains__ ('ipv6'): 
        print ("only ipv6")
        dat=parce(dat,'ipv6')
    if choice.value.__contains__ ('ipv4') :
        print ("only ipv4")
        dat=parce(dat,'ipv4')
    if choice.value.__contains__ ('all'): print ("do not exclude (dispay all)")   
    return (dat)
    

@app.get("/allbacklist",summary="generate all list contents",description=" see lists on allblackllist_dict")
def read_allblack(request: Request):
    client_host = request.client.host
    logge("allblacklists",client_host)
    black.getdb()
    print(black.db.values())
    urllist=list(black.db.values())
    ips=black.parceip(urllist)
    flatt= [item for sublist in ips for item in sublist]
    #ips = "\n\n".join(flattened)
    return (urllist,flatt)

@app.post("/db-blacklist/{listname}",summary="retrive individual list")
def read_dbblack(listname,request:Request): #choice2: TestQuery):
     #print (choice2.value)
     #print (black.db.keys())
     client_host = request.client.host
     logge(f'db-blacklist/{listname}',client_host)
     black.getdb()
     site= black.db[f'{listname}']
     print ("getting site:",site)
     sitel=[]
     sitel.append(site)
     ips=black.parceip(sitel)
     flatt = [item for sublist in ips for item in sublist]
     return (site,flatt)


@app.post("/db-blacklist_text/{listname}",summary="retrive individual list in plain text", response_class=PlainTextResponse)
def read_dbblackt(listname,request:Request): #choice2: TestQuery):
     #print (choice2.value)
     #print (black.db.keys())
     client_host = request.client.host
     logge(f'db-blacklist_text/{listname}',client_host)
     black.getdb()
     site= black.db[f'{listname}']
     print ("getting site:",site)
     sitel=[]
     sitel.append(site)
     ips=black.parceip(sitel)
     flatt = [item for sublist in ips for item in sublist]
     flatt=list(set(flatt))
     data2="\r\n".join(flatt)
     return (data2)


@app.post("/urlblacklist",summary="test url's site list")
def read_black(js: JsonFormatG,request:Request):
     client_host = request.client.host
     logge('urlblacklist',client_host)
     site= js['urllist']
     ips=black.parceip(site)
     flatt = [item for sublist in ips for item in sublist]
     return (flatt)

import os
@app.get("/allbacklist_dict",summary="get dictionary of actual lists")
def readdict(request:Request):
    client_host = request.client.host
    logge('allbacklist_dict',client_host)
    print(f"pid: {os.getpid()}")
    return (black.getdb())

@app.post("/addtoblacklist",summary="add items to the list")
def add_black(di:JsonFormatD,request:Request):
    client_host = request.client.host
    logge('addtoblacklist',client_host)
    print(f"pid: {os.getpid()}")
    black.putdb(di)
    return (black.getdb())

#@app.get("/load_dict",summary="load actual lists")

#@app.get("/store_dict",summary="presist actual lists")

# @app.get("/")
# def read_root():
#     """ Method Get Root
#         :return: Returns Hello World
#     """
#     #return ()
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     """ Method Get Item
#     :param item_id: item id to get
#     :param q: Operation (nor required, default None)
#     """
#     return {"item_id": item_id, "q": q}

# @app.post("/items/", status_code=201)
# def add_item(item: Item = Body(..., embed=True), status_code=201):
#     """ Add item
#       :param item: Item Class
#       :return: Returns operation result
#     """
#     return {"message": f"Item {item.item_id} with the name {item.item_name} has been added successfully."}

