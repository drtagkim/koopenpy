# Taekyung Kim(PhD)
# 2018-11-25
# Korean Open API Python Frontend
# for Pandas and KAIST students
import requests
import pandas as pd
import json
from urllib.parse import unquote
import xmltodict
class Bus:
    def __init__(self,service_key):
        self.service_key=unquote(service_key) #공공데이터 포털의 UTF-8 키
        self.endpoint='http://openapi.tago.go.kr/openapi/service/ArvlInfoInqireService'
        self.nogomsg="Service is not available."
        self.service_ok=False #for assertion
        self.r=None #python requests
    def access_data(self):
        assert self.service_ok, self.nogomsg
        r=self.r
        o=xmltodict.parse(r.content.decode())
        return o
    def collect(self):
        params={}
        params['ServiceKey']=self.service_key
        return params
    def call_request(self,url,params):
        r=requests.get(url,params=params)
        if r.status_code==200:
            self.service_ok=True
            self.r=r
        else:
            self.service_ok=False
            self.r=None
    def get_data(self):
        o=self.access_data() #데이터 접근
        try:
            i=o['response']['body']['items']['item']
            j=json.dumps(i)
            if isinstance(i,list):
                return pd.read_json(j)
            else:
                return pd.read_json('['+j+']')
        except KeyError:
            return None
        except TypeError:
            return None
    def get_page_no(self):
        o=self.access_data() #데이터 접근
        i=o['response']['body']['pageNo']
        return int(i)
    def get_total_count(self):
        o=self.access_data() #데이터 접근
        i=o['response']['body']['totalCount']
        return int(i)
class ButArrival(Bus):
    def __init__(self,service_key):
        super().__init__(service_key)
        self.service_url='/getSttnAcctoArvlPrearngeInfoList'
    def collect(self,city_code=25,node_id='DJB8001793ND'):
        params=super().collect()
        params['cityCode']=city_code
        params['nodeId']=node_id
        url=self.endpoint+self.service_url
        super().call_request(url,params)
class ButArrivalRoute(Bus):
    def __init__(self,service_key):
        super().__init__(service_key)
        self.service_url='/getSttnAcctoSpcifyRouteBusArvlPrearngeInfoList'
    def collect(self,city_code=25,node_id='DJB8001793ND',route_id='DJB30300002ND'):
        params=super().collect()
        params['cityCode']=city_code
        params['nodeId']=node_id
        params['routeId']=route_id
        url=self.endpoint+self.service_url
        super().call_request(url,params)
class ButCityCode(Bus):
    def __init__(self,service_key):
        super().__init__(service_key)
        self.service_url='/getCtyCodeList'
    def collect(self):
        params=super().collect()
        url=self.endpoint+self.service_url
        super().call_request(url,params)
