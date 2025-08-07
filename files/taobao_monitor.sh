#!/system/bin/sh

while true; do
    if ps -A -o NAME,WCHAN | awk '$1=="com.taobao.taobao" && $2=="ep_poll"{exit 1}'; then
        echo "Taobao not running, restarting..."
        am force-stop com.taobao.taobao
        am start -n com.taobao.taobao/com.taobao.tao.welcome.Welcome
        sleep 4
        ps -A -o PID,NAME,WCHAN | awk '$2=="com.taobao.taobao" && $3=="futex_wait_queue"' | awk '{print $1}' | xargs kill -9
    fi
    sleep 1
done