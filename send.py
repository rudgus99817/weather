import pickle
import requests
import re
#selection_list : 사용자의 선택정보 저장
#info(dict) : 추출한 날씨 정보를 날짜별로 저장한 dictionary
#지역코드 리스트 불러오기
wideCode = pickle.load(open('D:\\project\\weather\\wideCode.txt','rb'))
cityCode = pickle.load(open('D:\\project\\weather\\cityCode.txt','rb'))
dongCode = pickle.load(open('D:\\project\\weather\\dongCode.txt','rb'))

#dongCode에 대한 index 생성
def fdindex(selection_list):
	index = 0
	for i in range(selection_list[0]-1):
		index += len(cityCode[i])
	index += selection_list[1]-1
	return index
#숫자 입력을 통한 선택함수
def nselect(selection_list):
    for i in range(len(wideCode)):
        print (i+1,'. ',wideCode[i]['value'],sep='')
    selection_list.append(int(input()))
    for i in range(len(cityCode[selection_list[0]-1])):
        print (i+1,'. ',cityCode[selection_list[0]-1][i]['value'],sep='')
    selection_list.append(int(input()))
    index = fdindex(selection_list)
    for i in range(len(dongCode[index])):
        print (i+1,'. ',dongCode[index][i]['value'],sep='')
    selection_list.append(int(input(())))

#selection_list의 정보를 통해 request url 생성    
def makeurl(selection_list):
    dong = fdindex(selection_list)
    path = "http://www.kma.go.kr/weather/forecast/timeseries.jsp?searchType=INTEREST&"+'wideCode='+wideCode[selection_list[0]-1]['code']+'&'+'cityCode='+cityCode[selection_list[0]-1][selection_list[1]-1]['code']+'&'+'dongCode='+dongCode[dong][selection_list[2]-1]['code']
    return path
#requests모듈로 요청을 보내 웹페이지를 받아오는 함수    
def makerequest(path):
    r = requests.get(path)
    string = r.text
    return string
#웹페이지에서 필요한 날짜,날씨,시간정보 추출
def makeinfo(string):
    string = string[string.find('동네예보</caption>'):string.find('<tr class=\"degree')]
    day = re.findall("\d\d일 [^예,'(']",string)
    day.insert(0,'오늘')

    time = re.findall("title=\"\d\d시",string)
    time = [i.replace('title=\"','') for i in time]
    t = []
    t.append(time[:len(time)-16])
    t.append(time[len(time)-16:len(time)-8])
    t.append(time[len(time)-8:])

    weather = re.findall('PD_none\" title=\".....',string)
    weather = [i.replace('PD_none\" title=\"','') for i in weather]
    weather = [i.replace('\"','') for i in weather]
    weather = [i.replace('i','') for i in weather]
    weather = [i.replace('<','') for i in weather]
    weather = [i.replace('>','') for i in weather]
    weather.reverse()
    
    info=[]
    s=0
    for i in range(3):
        info.append({})
        info[i]['day'] = day[i]
        info[i]['time'] = t[i]
        info[i]['weather']=[]
        for j in range(len(info[i]['time'])-1):
            info[i]['weather'].append(weather.pop())
    
    return info
#모든 함수를 차례로 호출해서 하나의 함수호출로 info획득    
def getweather():
    selection_list = []
    nselect(selection_list)
    path = makeurl(selection_list)
    string = makerequest(path)
    info = makeinfo(string)
    return info    
#기존 정보를 최신정보로 업데이트
def update():
    
    
if(__name__ == '__main__'):
    info = getweather()
    print(info)
    