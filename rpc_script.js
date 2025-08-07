async function main(params) {
    return new Promise(function(resolve, reject) { 
        Java.perform(function () {
            try {
                // 1. 获取Android上下文
                var ActivityThread = Java.use("android.app.ActivityThread");
                var currentApplication = ActivityThread.currentApplication();
                var context = currentApplication.getApplicationContext();
                
                // 2. 获取Mtop类
                const Mtop = Java.use("mtopsdk.mtop.intf.Mtop");
                const HashMap = Java.use("java.util.HashMap");
                const MapEntry = Java.use('java.util.Map$Entry');
                
                // 3. 调用最简单的工厂方法
                var mtopInstance = Mtop.instance(context);

                const deviceId = mtopInstance.getDeviceId();
                const utdid = mtopInstance.getUtdid();
                const ttid = mtopInstance.getTtid();
                
                const mtopConfig = mtopInstance.getMtopConfig();
                const kqd = mtopConfig.sign.value;
                let n9f = Java.use("tb.n9f");
                var rMethod = n9f.r.overload(
                    "java.util.HashMap", 
                    "java.util.HashMap", 
                    "java.lang.String", 
                    "java.lang.String", 
                    "boolean", 
                    "java.lang.String"
                );
                const n9fVar = Java.cast(kqd, n9f);
                
                var hashMap = HashMap.$new();
                // 添加hashMap的键值对
                hashMap.put("data", params["data"]);
                hashMap.put("deviceId", deviceId);
                hashMap.put("sid", params["sid"]);
                hashMap.put("uid", params["uid"]);
                hashMap.put("x-features", "27");
                hashMap.put("appKey", params["appKey"]);
                hashMap.put("api", params["api"]);
                hashMap.put("mtopBusiness", "true");
                hashMap.put("utdid", utdid);
                hashMap.put("extdata", "openappkey=DEFAULT_AUTH");
                hashMap.put("ttid", ttid);
                hashMap.put("t", params["t"]);
                hashMap.put("v", params["v"]);
                
                // 3. 构造hashMap2参数
                var hashMap2 = HashMap.$new();
                hashMap2.put("pageId", "https://web.m.taobao.com/app/tb-trade/pay-it-for-me/index");
                hashMap2.put("pageName", "com.taobao.themis.container.app.TMSActivity");
                
                // 4. 其他参数
                var str = "21646297";
                var str2 = null;
                var z = false;
                var str3 = "r_45";

                var result = rMethod.call(n9fVar, hashMap, hashMap2, str, str2, z, str3);
                const resultMap = {};
                // 获取entrySet的迭代器（不需要显式转换Set类型）
                const iterator = result.entrySet().iterator();
                // 遍历打印所有键值对
                while (iterator.hasNext()) {
                    const entry = Java.cast(iterator.next(), MapEntry);
                    // 安全处理key和value
                    const key = entry.getKey();
                    const value = entry.getValue();
                    const keyStr = (key !== null) ? key.toString() : "null";
                    const valueStr = (value !== null) ? value.toString() : "null";
                    // console.log(`  ${keyStr} => ${encodeURIComponent(valueStr)}`);
                    resultMap[keyStr] = encodeURIComponent(valueStr);
                }
                resolve({...resultMap, deviceId, utdid, ttid});
            } catch (e) {
                console.log(e);
                reject(null);
            }
        });
    });
    
}

rpc.exports = { 
    main
};