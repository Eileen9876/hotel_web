#!/bin/bash

#============ 複製備份檔 ============#

dir="roomUseDate storeInfo";

for d in $dir
do 
    file=$(ls -1 ${BACKUP_DIR}/$d | sort -r | head -n 1)

    if [ -n "$file" ]; then
        cp ${BACKUP_DIR}/$d/$file data/$d.json
        echo COPY FILE ${BACKUP_DIR}/$d/$file
    fi
done

#============ 資料備份 ============#

cp ../usr/share/zoneinfo/Asia/Taipei ../etc/localtime # 更換時區

TIMESTAMP=$(date +'%Y%m%d%H%M')
SLEEP_TIME=60 # sec

while true
do 
    sleep ${SLEEP_TIME} # 服務尚未啟動，等服務啟動後再進行備份，避免備份空資料

    cp data/roomUseDate.json ${BACKUP_DIR}/roomUseDate/${TIMESTAMP}.json
    cp data/storeInfo.json ${BACKUP_DIR}/storeInfo/${TIMESTAMP}.json    

    echo backup success
done & # 背景執行

#============ 啟動服務 ============#

python api.py