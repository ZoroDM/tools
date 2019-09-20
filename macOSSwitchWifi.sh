#/bin/bash

echo "hahha"


#networksetup -setairportpower en0 off
#networksetup -setairportpower en0 on
#networksetup -setairportnetwork en0 world 08874151578
#networksetup -setairportnetwork en0 world 08874151578

n=100
while [ $n -ge 1 ] #或 while ((n>=1))
do
    echo $n
    let n-=1
    #关闭 wifi
    networksetup -setairportpower en0 off
    sleep 5
    networksetup -setairportpower en0 on
    #关闭wifi
    sleep 5
    #networksetup -setairportnetwork en0 world 08874151578
    #切换wifi
    #networksetup -setairportnetwork en0 world 08874151578

done