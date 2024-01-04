import json
import datetime
from ipaddress import IPv4Network, IPv6Network,ip_address
import ipaddress
import pymisp
import pprint

def is_valid_ip_address(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

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

def get_date_n_days_ago(n: int):
    today = datetime.date.today()
    delta = datetime.timedelta(days=n)
    date_n_days_ago = today - delta
    return date_n_days_ago.strftime("%Y.%m.%d")

def misp(days: int):
        # URL of the MISP instance
    misp_url = 'https://172.168.150.15'

    # Authentication key for the MISP instance
    misp_key = 'P8l0nvmVridvFDp2e3fJJVaNPMYRnsEJbFRBps6n'

# URL of the MISP instance
    misp_url1 = 'https://10.100.0.146'

# Authentication key for the MISP instance
    misp_key1 = '4caTm6uTWa0ovRrA4JgLjnJWIX0Lcprkx2TpFzF3'
    misp_key2 = 'E9wBg2CNNonCN9HzdXNJ7ittA4wiOfskflazRwL2'

    # Create a PyMISP object to interact with the MISP instance
    misp = pymisp.PyMISP(misp_url1, misp_key2, False)

    # Fetch all events from the MISP instance
    #events = misp.search(return_format='json',type_attribute='ip-src',date_from='2020-01-01')
    print ("init date:",get_date_n_days_ago(days))
    events = misp.search(return_format='json',type_attribute=['ip-dst','ip-src','url'],date_from=f'{get_date_n_days_ago(days)}')
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
   # write_list_to_file('ips.txt',ipsrct)
    print (ipsrct)
    ipsrct=list(set(ipsrct))
    data2="\r\n".join(ipsrct)
    return (data2)


out=misp(7)
print ("--------------------------")
print (out)