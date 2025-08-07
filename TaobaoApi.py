import time
import json
import requests
from urllib.parse import quote
from RpcClient import RpcClient

class TaobaoApi:
    def __init__(self, params):
        self.appKey = '21646297'
        self.uid = params['uid']
        self.sid = params['sid']
        self.userAgent = "MTOPSDK%2F3.1.1.7+%28Android%3B10%3BMeizu%3BM15%29+DeviceType%28Phone%29"
        self.headers = {
            'x-social-attr': '3',
            'x-sid': self.sid,
            'x-uid': self.uid,
            'x-nettype': 'WIFI',
            'Accept-Encoding': 'gzip',
            'x-pv': '6.3',
            'x-nq': 'WIFI',
            'x-region-channel': 'CN',
            'x-features': '27',
            'x-app-edition': 'ST',
            'x-app-conf-v': '0',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'cro-privacy-recommend-switch': 'open',
            'x-bx-version': '6.7.250602',
            'f-refer': 'mtop',
            'x-extdata': 'openappkey%3DDEFAULT_AUTH',
            'x-ttid': '231200%40taobao_android_10.51.0',
            'x-app-ver': '10.51.0',
            'nextrpc-req-id': '12',
            'x-c-traceid': '7PPXrEn3',
            'a-orange-dq': f'appKey={self.appKey}&appVersion=10.51.0&clientAppIndexVersion=1120250723094400661',
            'x-regid': 'reg0CCuA42juREMd2FelJL910cy3vyWB',
            'c-launch-info': '3,0,1753235630804,1753235304144,3',
            'x-appkey': self.appKey,
            'x-falco-id': '7PPXrEn3',
            'x-page-url': 'http%3A%2F%2Fm.taobao.com%2Findex.htm',
            'x-page-name': 'com.taobao.tao.welcome.Welcome',
            'user-agent': self.userAgent,
            'Host': 'trade-acs.m.taobao.com',
            'Connection': 'Keep-Alive'
        }
    def sign_and_update_headers(self, host, api, version, data):
        timestamp = str(int(time.time()))

        signParams = {
            "data": json.dumps(data),
            "sid": self.sid,
            "uid": self.uid,
            "appKey": self.appKey,
            "api": api,
            "t": timestamp,
            "v": version
        }

        rpcClient = RpcClient(packageName='com.taobao.taobao')
        signature = rpcClient.run(params=signParams)

        self.headers['x-sgext'] = signature['x-sgext']
        self.headers['x-sign'] = signature['x-sign']
        self.headers['x-mini-wua'] = signature['x-mini-wua']
        self.headers['x-umt'] = signature['x-umt']
        self.headers['x-devid'] = signature['deviceId']
        self.headers['x-utdid'] = quote(signature['utdid'], safe='')
        self.headers['x-ttid'] = signature['ttid']
        self.headers['x-t'] = timestamp
        self.headers['Host'] = host
    
    def queryboughtlist(self):
        host = 'trade-acs.m.taobao.com'
        api = 'mtop.taobao.order.queryboughtlist.stream'
        version = '1.0'
        # 基础URL
        url = f"https://{host}/gw/{api}/{version}/"

        data = {
            "OrderType":"OrderList",
            "appName":"tborder",
            "appVersion":"3.0",
            "condition":{
                "deviceLevel":"low",
                "installApp":"WX",
                "openFrom":"mytao",
                "rootTabCode":"all",
                "version":"1.0.0"
            },
            "forceBoughtlist4":"true",
            "page":"1",
            "tabCode":"waitPay" # waitConfirm 待收货，waitPay 待付款
        }

        self.sign_and_update_headers(host=host, api=api, version=version, data=data)
        
        # 发送POST请求
        response = requests.post(url, headers=self.headers, data={'data': json.dumps(data) }, timeout=(5,10))
        
        return json.loads(response.content)
    def orderget(self, orderId):
        host = 'acs.m.taobao.com'
        api = 'mtop.taobao.paying.new.order.get'
        version = '1.0'
        
        url = f"https://{host}/gw/{api}/{version}/"

        data = {
            "orderId": orderId
        }

        self.sign_and_update_headers(host=host, api=api, version=version, data=data)

        response = requests.get(url=url, headers=self.headers, params={"data": json.dumps(data)}, timeout=(5,10))
        return json.loads(response.content)
    
    def dopay(self, orderId):
        host = 'guide-acs.m.taobao.com'
        api = 'mtop.order.dopay'
        version = '4.0'

        url = f'https://{host}/gw/{api}/{version}/'

        data = {
            "code":"batchConfirmGoods",
            "noNeedPwd":"true",
            "openFrom":"orderListNoBatchPopSingle",
            "orderId":orderId,
            "payParams":{
                f"{orderId}":"{\"action\":\"commonAction\",\"originalCode\":\"confirmGood\"}"
            }
        }

        print(data)

        self.sign_and_update_headers(host=host, api=api, version=version, data=data)

        response = requests.get(url=url, headers=self.headers, params={"data": json.dumps(data)}, timeout=(5,10))
        return json.loads(response.content)
    
    def detail(self):
        host = 'trade-acs.m.taobao.com'
        api = 'mtop.taobao.detail.data.get'
        version = '1.0'
        # 基础URL
        url = f"https://{host}/gw/{api}/{version}/"

        data = {
            "detail_v":"3.3.2",
            "exParams":"{\"appReqFrom\":\"detail\",\"container_type\":\"xdetail\",\"countryCode\":\"CN\",\"cpuCore\":\"8\",\"cpuMaxHz\":\"null\",\"deviceLevel\":\"low\",\"dinamic_v3\":\"true\",\"downgrade_new_detail\":\"true\",\"dynamicJsonData\":\"true\",\"entryUtParam\":\"{\\\"x_object_type\\\":\\\"item\\\",\\\"pvid\\\":\\\"ab717762-fcff-41b8-95d5-41bf8ccf766b\\\",\\\"sessionid\\\":\\\"ab717762-fcff-41b8-95d5-41bf8ccf766b\\\",\\\"x_ad\\\":\\\"0\\\",\\\"x_object_id\\\":\\\"754253066490\\\"}\",\"finalUltron\":\"true\",\"from\":\"newDetail\",\"id\":\"754253066490\",\"industryMainPicDegrade\":\"false\",\"isFoldDevice\":\"false\",\"isPadDevice\":\"false\",\"item_id\":\"754253066490\",\"latitude\":\"0\",\"liveAutoPlay\":\"true\",\"longitude\":\"0\",\"newStruct\":\"true\",\"nick\":\"tb7463288608\",\"openFrom\":\"pagedetail\",\"originalHost\":\"item.taobao.com\",\"osVersion\":\"34\",\"phoneType\":\"Pixel 7\",\"preload_v\":\"industry\",\"scm\":\"1007.13175.433702.691730_689565_514326_467908_473436_449461_453509_456622_456324_456468_456831_457997_458434_458461_462686_459493_460483_460551_462548_463036_463104_463729_463823_463998_464896_465353_465442_465651_465986_460740_466253_466281_466703_467452_468088_468194_468257_468374_468758_469790_469915_471638_472308_473271_474374_474464_474965_475448_476248_477325_477706_479106_482063_484427_484421_484423_486006_486917_488821_491151_491525_489415_490073_492099_492243_492840_497200_493727_495174_495432_496476_498423_498687_504624_499807_499972_501587_507684_502843_503678_504191_506159_506664_506731_507166_507988_509012_510092_511431_511797_511973_491982_487102_675375_693350_693822_519253_514542_520606_518937_503961_517133_503080_499658_504345_500922_507048_502092_512505\",\"screenHeight\":\"2201\",\"screenWidth\":\"1080\",\"soVersion\":\"2.0\",\"spm-cnt\":\"a2141.7631564\",\"supportIndustryMainPic\":\"true\",\"ttd_ttid\":\"231200@tt_detail_android_10.50.10\",\"ultron2\":\"true\",\"upStreamPrice\":\"4880\",\"utdid\":\"aILU7kVXTBUDAN5Er0jq3fqU\",\"videoAutoPlay\":\"false\",\"xxc\":\"home_recommend\"}","id":"754253066490"}

        self.sign_and_update_headers(host=host, api=api, version=version, data=data)
        
        response = requests.get(url=url, headers=self.headers, params={"data": json.dumps(data)}, timeout=(5,10))
        return json.loads(response.content)