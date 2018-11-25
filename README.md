# koopenpy
한국 공공데이터 포털 파이썬 프런트 엔드

# 사용하기 전에
```
pip install -r requirement.txt
```

# 설치&업그레이드
## 최초 설치
```
pip install http://github.com/drtagkim/koopenpy/zipball/master
```

## 업그레이드
```
pip install --upgrade http://github.com/drtagkim/koopenpy/zipball/master
```


# 예제
## 관광공사 API
```
from koopenpy.tour import KorTourKeywordSearch
service_key="..." #여러분의 Service Key(공공데이터 포털의 UTF-8형식 코드)
test=KorTourKeywordSearch(service_key)
test.collect("제주도")
test.get_data() #Pandas의 DataFrame으로 반환합니다.
test.get_data().to_clipboard(index=False)
#엑셀에서 붙여넣기 해 보세요.
```

