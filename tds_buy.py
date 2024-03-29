import requests, json, time, datetime, html, re, os, sys
from keep_alive import keep_alive
class OOP:
    def __init__(self, TDS_token, idfb, cookie):
        self.TDS_token = TDS_token
        self.idfb = idfb
        self.cookie = cookie
        self.xuHienTai = 0
        self.STT = 0
        self.xuHienTai = 0
        self.STT = 0
        self.s = requests.Session()
    def layThongTinAcc(self):
        url = 'https://traodoisub.com/api/?fields=profile&access_token={0}'.format(self.TDS_token)
        response = self.s.get(url)
        dataLTT =  json.loads(response.text)
        if('error' in dataLTT):
            print('Token tds die !!!')
            exit()
        else:
            user = dataLTT['data']['user']
            xu = dataLTT['data']['xu']
            xudie = dataLTT['data']['xudie']
            self.xuHienTai += int(xu)
            print(f'User : {user} | Xu : {xu} | Xu die : {xudie}')

    def datCauHinh(self): 
        url = 'https://traodoisub.com/api/?fields=run&id={0}&access_token={1}'.format(self.idfb, self.TDS_token)
        response = self.s.get(url)
        dataDCH =  json.loads(response.text)
        if 'error' in dataDCH:
            print(dataDCH['error'])
            exit()
        else:    
            idFB = dataDCH['data']['id']
            msgTT = dataDCH['data']['msg']
            print(f'ID : {idFB} | Trạng thái : {msgTT}')
     
    def layNhiemVu(self):
        url = 'https://traodoisub.com/api/?fields=reaction&access_token={0}'.format(self.TDS_token)
        response = self.s.get(url)
        data =  json.loads(response.text)
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            print("Error decoding JSON response.")
            return
        arr_id_value = []
        arr_type_value = []
        for item in data:
            if 'error' in item and 'countdown' in item:
                countdown = int(item['countdown'])
                for i in range(countdown, 0, -1):
                    print(f'Thao tác quá nhanh vui lòng chậm lại, đợi {i} giây', end='\r')
                    time.sleep(1)
            elif 'id' in item:
                id_value = item['id']
                type_value = item['type']
                arr_id_value.append(id_value)
                arr_type_value.append(type_value) 
                for i in range(len(arr_id_value)):
                    type_value = arr_type_value[i]
                    id_value = arr_id_value[i]
                    self.reaction(id_value, type_value)
                    self.nhanXu(id_value, type_value)
                    del arr_id_value[i]
                    del arr_type_value[i]
            elif 'error' in item and 'time_reset' in item:
                print('Đổi cookie mới')
                exit()
            else:
                return
    def nhanXu(self, id_value, type_value):
        now = datetime.datetime.now()
        base_url = f"https://traodoisub.com/api/coin/?type={type_value}&id={id_value}&access_token={self.TDS_token}"
        response = self.s.get(base_url)
        if response.status_code == 200:
            dataNX = response.json()
            if 'data' in dataNX:
                msg = dataNX['data']['msg']
                xuTong = int(re.search(r'\d+', msg).group())
                self.xuHienTai += xuTong
                self.STT+= 1
                print('[' + str(self.STT) + '] | ' + str(now.strftime("%H:%M:%S")) + ' | ' + 'ID : ' + str(id_value) + '  | ' + 'Trạng thái : ' + str(type_value) + ' | + ' + str(xuTong) + ' | ' + 'Xu hiện tại : ' + str(self.xuHienTai))
                if (self.STT == answer):
                    self.nghiChongBlock(chongBlock)
                else:
                    self.delay(seconds)
            else:
                pass

        else:
            print('not 200')
    def reaction(self, id_value, type_value):
        urlReaction = 'https://mbasic.facebook.com/reactions/picker/?is_permalink=1&ft_id={}'.format(id_value)
        headers = {
            'authority' : 'mbasic.facebook.com',
            'method' : 'GET',
            'path' : '/reactions/picker/?is_permalink=1&ft_id={}'.format(id_value),
            'scheme' : 'https',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'vi',
            'Cache-Control' : 'max-age=0',
            'Cookie': self.cookie,
            'Sec-Ch-Ua' : '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'Sec-Ch-Ua-Full-Version-List' : '"Google Chrome";v="117.0.5938.150", "Not;A=Brand";v="8.0.0.0", "Chromium";v="117.0.5938.150"',
            'Sec-Ch-Ua-Mobile' : '?0',
            'Sec-Ch-Ua-Model' : '""',
            'Sec-Ch-Ua-Platform' : '"Windows"',
            'Sec-Ch-Ua-Platform-Version' : '"15.0.0"',
            'Sec-Fetch-Dest' : 'document',
            'Sec-Fetch-Mode' : 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User' : '?1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'           
            }
        r = requests.get(urlReaction, headers= headers)
        text = r.text
        # try:
        try:
            if type_value == 'LIKE':
                    splitTextLike = text.split('<a href="/ufi/reaction/?')[1].split('"')[0]
                    urlLike = 'https://mbasic.facebook.com/ufi/reaction/?{}'.format(html.unescape(splitTextLike))
                    r = requests.get(urlLike, headers= headers)
                    check = r.text
                    should_exit = self.checkBlock(check)
                    if should_exit:
                        exit()
            elif type_value == 'LOVE':
                    splitTextLike = text.split('<a href="/ufi/reaction/?')[2].split('"')[0]
                    urlLike = 'https://mbasic.facebook.com/ufi/reaction/?{}'.format(html.unescape(splitTextLike))
                    r = requests.get(urlLike, headers= headers)
                    check = r.text
                    should_exit = self.checkBlock(check)
                    if should_exit:
                        exit()
            elif type_value == 'CARE':
                    splitTextLike = text.split('<a href="/ufi/reaction/?')[3].split('"')[0]
                    urlLike = 'https://mbasic.facebook.com/ufi/reaction/?{}'.format(html.unescape(splitTextLike))
                    r = requests.get(urlLike, headers= headers)
                    check = r.text
                    should_exit = self.checkBlock(check)
                    if should_exit:
                        exit()         
            elif type_value == 'HAHA':
                    splitTextLike = text.split('<a href="/ufi/reaction/?')[4].split('"')[0]
                    urlLike = 'https://mbasic.facebook.com/ufi/reaction/?{}'.format(html.unescape(splitTextLike))
                    r = requests.get(urlLike, headers= headers)
                    check = r.text
                    should_exit = self.checkBlock(check)
                    if should_exit:
                        exit()
            elif type_value == 'WOW':
                    splitTextLike = text.split('<a href="/ufi/reaction/?')[5].split('"')[0]
                    urlLike = 'https://mbasic.facebook.com/ufi/reaction/?{}'.format(html.unescape(splitTextLike))
                    r = requests.get(urlLike, headers= headers)
                    check = r.text
                    should_exit = self.checkBlock(check)
                    if should_exit:
                        exit()
            elif type_value == 'SAD':
                    splitTextLike = text.split('<a href="/ufi/reaction/?')[6].split('"')[0]
                    urlLike = 'https://mbasic.facebook.com/ufi/reaction/?{}'.format(html.unescape(splitTextLike))
                    r = requests.get(urlLike, headers= headers)
                    check = r.text
                    should_exit = self.checkBlock(check)
                    if should_exit:
                        exit()
            elif type_value == 'ANGRY':
                    splitTextLike = text.split('<a href="/ufi/reaction/?')[7].split('"')[0]
                    urlLike = 'https://mbasic.facebook.com/ufi/reaction/?{}'.format(html.unescape(splitTextLike))
                    r = requests.get(urlLike, headers= headers)
                    check = r.text
                    should_exit = self.checkBlock(check)
                    if should_exit:
                        exit()
        except:
            pass
    def checkBlock(self, check):
        try:
            if splitCheck in check:
                splitCheck = check.split('<div class="bn bo bp j bq"><span class="br"><div>')[1].split('<br /><br />')[0]
                print(splitCheck)
                return "specific content" in splitCheck
            else:
                pass
        except:
            pass
    def delay(self, seconds):
        for i in range(seconds, 0, -1):
            print(f'Vui lòng đợi sau -> {str(i)} giây', end='\r')
            time.sleep(1)
    def nghiChongBlock(self, chongBlock):
        for i in range(chongBlock, 0, -1):
            print(f'Đang nghỉ chống block, vui lòng đợi sau -> {str(i)} giây', end='\r')
            time.sleep(1)
            
keep_alive()
TDS_token = os.getenv("Token")
idfb = 61554282509974
cookie = os.getenv("Cookie")
seconds = 3 #time delay
answer = 120 #Count nv
chongBlock =120 #Time antiblock
api = OOP(TDS_token, idfb, cookie)
api.layThongTinAcc()
api.datCauHinh()
while(True):
    api.layNhiemVu()