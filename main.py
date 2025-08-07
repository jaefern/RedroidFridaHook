from TaobaoApi import TaobaoApi
        
if __name__ == "__main__":
    params = {
        "uid": "2206539236005",
        "sid": "2d1780561d05a1e8939b0985623807a6"
    }
    taobaoApi = TaobaoApi(params=params)
    host = 'trade-acs.m.taobao.com'
    api = 'mtop.taobao.order.queryboughtlist.stream'
    version = '1.0'
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
    taobaoApi.sign_and_update_headers(host, api, version, data)
    print(taobaoApi.headers)