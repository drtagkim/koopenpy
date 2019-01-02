# Taekyung Kim(PhD)
# Gyunggi-bus API - how to know WGS84 coordinations
import requests
import pandas as pd
import json
from urllib.parse import unquote
import xmltodict
class GBus:
    '''
>>> my_key='....'
>>> bus=GBus(my_key)
>>> bus.collect(15414)
>>> bus.filter_station(214000424)
(36.97805, 127.0438333)
    '''
    def __init__(self,service_key):
        self.service_key=unquote(service_key)
        self.endpoint='http://openapi.gbis.go.kr/ws/rest'
        self.service_url="/busstationservice"
        self.nogomsg="Service is not available."
        self.service_ok=False #for assertion
        self.r=None #python requests
    def access_data(self):
        assert self.service_ok, self.nogomsg
        r=self.r
        o=xmltodict.parse(r.content.decode())
        return o
    def collect(self,keyword):
        params={}
        params['serviceKey']=self.service_key
        params['keyword']=keyword
        self.params=params
        url=self.endpoint+self.service_url
        self.call_request(url,params)
    def filter_station(self,stationId):
        df=self.get_data()
        df1=df.loc[df['stationId']==stationId,:]
        lon=float(df1['x']);lat=float(df1['y'])
        return lat,lon
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
        self.o=o
        try:
            i=o['response']['msgBody']['busStationList']
            j=json.dumps(i)
            if isinstance(i,list):
                return pd.read_json(j)
            else:
                return pd.read_json('['+j+']')
        except KeyError:
            return None
        except TypeError:
            return None