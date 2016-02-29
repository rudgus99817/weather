import pickle
import requests
import re
wideCode = pickle.load(open('D:\\project\\weather\\wideCode.txt','rb'))
cityCode = pickle.load(open('D:\\project\\weather\\cityCode.txt','rb'))
dongCode = pickle.load(open('D:\\project\\weather\\dongCode.txt','rb'))


def fdindex(selection_list):
	index = 0
	for i in range(selection_list[0]-1):
		index += len(cityCode[i])
	index += selection_list[1]-1
	return index

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

    
def makeurl(selection_list):
    dong = fdindex(selection_list)
    path = "http://www.kma.go.kr/weather/forecast/timeseries.jsp?searchType=INTEREST&"+'wideCode='+wideCode[selection_list[0]-1]['code']+'&'+'cityCode='+cityCode[selection_list[0]-1][selection_list[1]-1]['code']+'&'+'dongCode='+dongCode[dong][selection_list[2]-1]['code']
    return path

def factory(string):
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

if(__name__ == '__main__'):
    selection_list = []
    nselect(selection_list)
    path = makeurl(selection_list)
    r = requests.get(path)
    string = r.text
    print(factory(string))
    