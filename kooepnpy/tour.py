# Taekyung Kim(PhD)
# 2018-11-25
# Korean Open API Python Frontend
# for Pandas and KAIST students
import requests
import pandas as pd
import json
from urllib.parse import unquote
import xmltodict
class KorTour:
    def __init__(self,service_key):
        self.service_key=unquote(service_key) #공공데이터 포털의 UTF-8 키
        self.endpoint='http://api.visitkorea.or.kr/openapi/service/rest/KorService'
        self.nogomsg="Service is not available."
        self.service_ok=False #for assertion
        self.r=None #python requests
        self.contentType=self.create_content_type()
    def create_content_type(self):
        contentType={}
        contentType['attraction']=12 #관광지
        contentType['culture']=14 #문화시설
        contentType['festival']=15 #축제공연행사
        contentType['cource']=25 #여행코스
        contentType['reports']=28 #레포츠
        contentType['accomodation']=32 #숙박
        contentType['shopping']=38 #쇼핑
        contentType['food']=39 #음식
        return contentType
    def show_content_type(self):
        return self.contentType.keys()
    def access_data(self):
        assert self.service_ok, self.nogomsg
        r=self.r
        o=xmltodict.parse(r.content.decode())
        return o
    def collect(self):
        params={}
        params['ServiceKey']=self.service_key
        params['MobileOS']='ETC'
        params['MobileApp']='AppTest'
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
class KorTourRegionCode(KorTour):
    def __init__(self,service_key):
        super().__init__(service_key)
        self.service_url='/areaCode'
    def collect(self,num_of_rows=10,page_no=1,area_code=1):
        params=super().collect()
        params['numOfRows']=num_of_rows
        params['pageNo']=page_no
        params['areaCode']=area_code
        url=self.endpoint+self.service_url
        super().call_request(url,params)
class KorTourKeywordSearch(KorTour):
    def __init__(self,service_key):
        super().__init__(service_key)
        self.service_url="/searchKeyword"
    def collect(self,keyword,num_of_rows=10,list_yn='Y',arrange='A',content_type='',cat1=''):
        params=super().collect()
        params['numOfRows']=num_of_rows
        params['listYN']=list_yn
        params['arrange']=arrange
        params['contentTypeId']=content_type
        params['keyword']=keyword
        url=self.endpoint+self.service_url
        super().call_request(url,params)
class KorTourAreaCode(KorTour):
    def __init__(self,service_key):
        super().__init__(service_key)
        self.service_url="/areaCode"
    def collect(self,areacode=''):
        params=super().collect()
        params['areaCode']=areacode
        url=self.endpoint+self.service_url
        super().call_request(url,params)
class KorTourCategoryCode(KorTour):
    def __init__(self,service_key):
        super().__init__(service_key)
        self.service_url="/categoryCode"
    def collect(self):
        params=super().collect()
        url=self.endpoint+self.service_url
        super().call_request(url,params)
class KorTourSearchFestival(KorTour):
    def __init__(self,service_key):
        super().__init__(service_key)
        self.service_url="/searchFestival"
    def collect(self,event_start_date=''):
        params=super().collect()
        params['eventStartDate']=event_start_date
        url=self.endpoint+self.service_url
        super().call_request(url,params)
class KorTourSearchStay(KorTour):
    def __init__(self,service_key):
        super().__init__(service_key)
        self.service_url="/searchStay"
    def collect(self,area_code='',sigungu_code=''):
        params=super().collect()
        params['areaCode']=area_code
        params['sigunguCode']=sigungu_code
        url=self.endpoint+self.service_url
        super().call_request(url,params)
class KorTourAreaBasedList(KorTour):
    def __init__(self,service_key):
        super().__init__(service_key)
        self.service_url="/areaBasedList"
    def collect(self,area_code='',sigungu_code='',content_type_id=''):
        params=super().collect()
        params['areaCode']=area_code
        params['sigunguCode']=sigungu_code
        params['contentTypeId']=content_type_id
        url=self.endpoint+self.service_url
        super().call_request(url,params)
class KorTourLocationBasedList(KorTour):
    def __init__(self,service_key):
        super().__init__(service_key)
        self.service_url="/locationBasedList"
    def collect(self,longitude=126.5835,latitude=37.1233,radius=5000,content_type_id=''):
        params=super().collect()
        params['contentTypeId']=content_type_id
        params['mapX']=longitude
        params['mapY']=latitude
        params['radius']=radius
        url=self.endpoint+self.service_url
        super().call_request(url,params)
class KorTourDetailIntro(KorTour):
    def __init__(self,service_key):
        super().__init__(service_key)
        self.service_url="/detailIntro"
    def collect(self,content_id=1118680,content_type_id=15):
        params=super().collect()
        params['contentId']=content_id
        params['contentTypeId']=content_type_id
        url=self.endpoint+self.service_url
        super().call_request(url,params)
class KorTourDetailImage(KorTour):
    def __init__(self,service_key):
        super().__init__(service_key)
        self.service_url="/detailImage"
    def collect(self,content_id=1118680):
        params=super().collect()
        params['contentId']=content_id
        url=self.endpoint+self.service_url
        super().call_request(url,params)
