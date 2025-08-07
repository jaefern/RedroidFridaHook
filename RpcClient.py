import subprocess
import time
import frida

class RpcClient:
    def __init__(self, packageName):
        self.packageName = packageName
        try:
            subprocess.run(["adb", "root"])
        except Exception as e:
            print(f"Error: {e}")
            return
        
    def reboot_frida(self):
        try:
            subprocess.run(["adb", "shell", "kill -9 $(pidof frida-server)"])
            time.sleep(5)
        except Exception as e:
            print(f"Error: {e}")
            return
        
    def get_pid(self, device):
        # 方法1：通过Frida枚举
        processes = device.enumerate_processes()
        taobao_process = [p for p in processes if p.name == self.packageName]
        if len(taobao_process) > 0:
            return taobao_process[0].pid
        
        # 方法2：通过adb命令获取
        try:
            import subprocess
            output = subprocess.check_output(["adb", "shell", "pidof", self.packageName])
            return int(output.decode().strip())
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    def run(self, params):
        tryCount = 3
        while True:
            try:
                # 连接设备
                device = frida.get_usb_device()
                
                pid = self.get_pid(device)
                
                session = device.attach(pid)

                # 加载RPC脚本
                with open("rpc_script.js", "r", encoding="utf-8") as f:
                    script = session.create_script(f.read())
                script.load()

                script.on("message", lambda message, _: print(message))

                # 远程调用
                signature = script.exports_sync.main(params)
                return signature
            except Exception as e:
                print(e)
                tryCount -= 1
                if tryCount <= 0:
                    self.reboot_frida()
                    print("Reboot frida")
                time.sleep(1)
                continue