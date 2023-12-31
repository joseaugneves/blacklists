import pprint
import json

class fastapi_vars:
    
    file='datavar'
    me={}   # {'varname':value,'varname':value,....}

    def read_dict_f(filen):
        dictionary={}
        try :
            with open(filen, 'r') as file:
                data = file.read()
                dictionary = json.loads(data)
        except : dictionary={}
        return dictionary

    def write_dict_f(dic, filen):
        with open(filen, 'w') as file:
            json.dump(dic, file)


    def getvars():
        fastapi_vars.me=fastapi_vars.read_dict_f(fastapi_vars.file)
        return list(fastapi_vars.me.keys())
    
    
    def addvar (name,val):
        fastapi_vars.me=fastapi_vars.read_dict_f(fastapi_vars.file)
        fastapi_vars.me.update({name:val})
        fastapi_vars.write_dict_f(fastapi_vars.me,fastapi_vars.file)
        return
    
    def getvar (name):
        fastapi_vars.me=fastapi_vars.read_dict_f(fastapi_vars.file)
        return fastapi_vars.me[name]
    
    
# vars=fastapi_vars
# data1=[1,2,3,4,5,6]
# data2={'a':1,'b':2}
# vars.addvar('data',data1)
# vars.addvar('dat',data2)
# vars.addvar('name','jose')
# pprint.pprint (vars.getvars())
# print("")
# pprint.pprint (vars.getvar('data'))
# print("")
# pprint.pprint (vars.getvar('dat'))
# print("")
# pprint.pprint (vars.getvar('name'))