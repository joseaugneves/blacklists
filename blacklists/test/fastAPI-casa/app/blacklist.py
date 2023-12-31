
import requests
from ipaddress import IPv4Network, IPv6Network,ip_address
import pprint
import re
import json
import datetime
import ipaddress
import pymisp

def read_dict_f(filen):
    with open(filen, 'r') as file:
        data = file.read()
        dictionary = json.loads(data)
    return dictionary

def write_dict_f(dic, filen):
    with open(filen, 'w') as file:
        json.dump(dic, file)

db={
    'Tenable':'https://docs.tenable.com/vulnerability-management/Content/Settings/Sensors/CloudSensors.htm',
    'shodan':'https://wiki.ipfire.org/configuration/firewall/blockshodan',
    #'qualys':'https://qualys.my.site.com/discussions/s/article/000005823',
    #'censys2':'https://support.censys.io/hc/en-us/articles/360043177092-from-faq',
    'censys':'https://support.censys.io/hc/en-us/article_attachments/20618695168532'
}

def getdb():
    global db
    try:
        db=read_dict_f('data')
    except:
        print("notting to read")
    return(db)

def putdb(dic):
    db.update(dic['dictionary'])
    write_dict_f(db,"data")

def validate_ip_network(address):
    try:
        IPv4Network(address)
        return True
    except ValueError:
        try:
            IPv6Network(address)
            return True
        except ValueError:
            return False

def validate_ip_address(address):
    try:
        ip_address(address)
        return True
    except ValueError:
        return False

def detectipv4(data):
    ipv=['1','2','3','4','5','6','7','8','9','0','.','/']
    out=""
    outlist=[]
    for e in list(data) :
        if e in ipv : out=out+e
        else :
            if len(out)>8 :
                outlist.append(out)
            out=""
    if len(out)>8 : outlist.append(out)
    control=0
    ips=[]
    for e in outlist :
        if validate_ip_address(e) :
            ips.append(e)
            control=control+1
        if validate_ip_network(e) :
            if '/' in e :ips.append(e)
            control=control+1
    return control,ips

def detectipv6(data):
    ipv=['1','2','3','4','5','6','7','8','9','0','A','B','C','D','E','F',':','/','a','b','c','d','e','f']
    out=""
    outlist=[]
    for e in list(data) :
        if e in ipv : out=out+e
        else :
            if len(out)>8 :
                outlist.append(out)
            out=""
    if len(out)>8 : outlist.append(out)
    control=0
    ips=[]
    for e in outlist :
        if validate_ip_address(e) :
            ips.append(e)
            control=control+1
        if validate_ip_network(e) :
            if '/' in e :ips.append(e)
            control=control+1
    return control,ips

def parceip(data):

    ips=[]
    for f in data :
        response = requests.get(f)
        print (f"url:f{f} - ",response)
        dat = response.text
        da=dat.split(' ')
        da=list(set(da))
        for e in da :
            rep,ip=detectipv6 (e)
            if rep >0:ips.append (ip)
            rep,ip=detectipv4 (e)
            if rep >0:ips.append (ip)
    return ips

def get_date_n_days_ago(n: int):
    today = datetime.date.today()
    delta = datetime.timedelta(days=n)
    date_n_days_ago = today - delta
    return date_n_days_ago.strftime("%Y.%m.%d")


def is_valid_ip_address(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def write_list_to_file(file_path, a_list):
    with open(file_path, "w") as file:
        for item in a_list:
            file.write("%s\n" % item)

def misp(days: int):
        # URL of the MISP instance
    misp_url = 'https://172.168.50.5'

    # Authentication key for the MISP instance
    misp_key = 'P8l0nvmVridvFDp2e3fJJVaNPMYRnsEJbFRBps6n'

    # Create a PyMISP object to interact with the MISP instance
    misp = pymisp.PyMISP(misp_url, misp_key, False)

    # Fetch all events from the MISP instance
    #events = misp.search(return_format='json',type_attribute='ip-src',date_from='2020-01-01')
    print ("init date:",get_date_n_days_ago(days))
    events = misp.search(return_format='json',type_attribute='url',date_from=f'{get_date_n_days_ago(days)}')
    # Loop through each event and display all IP artifacts
    #print (type(events))
    #pprint.pprint (events)
    print ("----------------------------------------------------------------------------------------------------------------------------------------------------------")
    print ("----------------------------------------------------------------------------------------------------------------------------------------------------------")
    print ("----------------------------------------------------------------------------------------------------------------------------------------------------------")
    print ("----------------------------------------------------------------------------------------------------------------------------------------------------------")
    print ("----------------------------------------------------------------------------------------------------------------------------------------------------------")
    tcount=0
    isurl=0
    ipsrct=[]
    for event in events:
        e = event['Event']
        id=e['id']
        dat=e['date']
        times=e['timestamp']
        nameorg=e['Org']['name']
        nameorgc=e['Orgc']['name']
        ipsrc=[]
        count=0
        for ii in e['Attribute']:
            if '/' in ii['value']: 
                isurl=isurl+1   
            if '\\' in ii['value']: 
                isurl=isurl+1
            if is_valid_ip_address(ii['value']):
                ipsrc.append(ii['value'])
                ipsrct.append(ii['value'])
                count=count+1
        #print (nameorg,nameorgc,ipsrc)
        data={'date':dat,'timestamp':times,'id':id,'data':{'name_org':nameorg,'nameorgc':nameorgc,'atribute_src':ipsrc,'atrib_count':count}}
        pprint.pprint (data)
        tcount=tcount+count
    print(f"total attributes ip procecced={tcount} ulr={isurl}")   
    write_list_to_file('ips.txt',ipsrct)
    print (ipsrct)
    ipsrct=list(set(ipsrct))
    data2="\r\n".join(ipsrct)
    return (data2)

#urilist=['https://wiki.ipfire.org/configuration/firewall/blockshodan','https://qualys.my.site.com/discussions/s/article/000005823','https://support.censys.io/hc/en-us/articles/360043177092-from-faq','https://docs.tenable.com/vulnerability-management/Content/Settings/Sensors/CloudSensors.htm']
#urllist=["https://qualys.my.site.com/discussions/s/article/000005823"]
#ips=parceip(urllist)
#print (ips)
#print(misp(7))
