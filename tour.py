import requests
import pandas as pd
import json
from urllib.parse import unquote
import xmltodict
class KorTour:
    def __init__(self):
        self.endpoint='http://api.visitkorea.or.kr/openapi/service'
        self.nogomsg="Service is not available."
        self.service_ok=False #for assertion
        self.r=None #python requests
    def access_data(self):
        assert self.service_ok, self.nogomsg
        r=self.r
        o=xmltodict.parse(r.content.decode())
        return o
class KorTourRegionCode(KorTour):
    def __init__(self,service_key):
        super().__init__()
        self.service_url='/rest/KorService/areaCode'
        self.service_key=unquote(service_key) #공공데이터 포털의 UTF-8 키
    def collect(self,num_of_rows=10,page_no=1,area_code=1):
        params={}
        params['ServiceKey']=self.service_key
        params['numOfRows']=num_of_rows
        params['pageNo']=page_no
        params['MobileOS']='ETC'
        params['MobileApp']='AppTest'
        params['areaCode']=area_code
        r=requests.get(self.endpoint+self.service_url,params=params)
        if r.status_code==200:
            self.service_ok=True
            self.r=r
    def get_data(self):
        o=self.access_data() #데이터 접근
        i=o['response']['body']['items']['item']
        j=json.dumps(i)
        return pd.read_json(j)
    def get_page_no(self):
        o=self.access_data() #데이터 접근
        i=o['response']['body']['pageNo']
        return int(i)
    def get_total_count(self):
        o=self.access_data() #데이터 접근
        i=o['response']['body']['totalCount']
        return int(i)