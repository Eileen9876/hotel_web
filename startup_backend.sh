#!/bin/bash

#============ 複製備份檔 ============#

dir="room_usage_date"; # 多個資料夾 dir="room_usage_date store_info";

for d in $dir
do 
    if [ -d "${BACKUP_DIR}/$d" ]; then
        # 資料夾存在，複製最新的備份檔，備份檔以創建日期命名 YYYYmmddHH
        
        file=$(ls -1 ${BACKUP_DIR}/$d | sort -r | head -n 1)

        if [ -n "$file" ]; then
            cp ${BACKUP_DIR}/$d/$file data/$d.json
            echo COPY FILE ${BACKUP_DIR}/$d/$file TO data/$d.json
        fi
    else
        # 資料夾不存在，創建資料夾

        mkdir ${BACKUP_DIR}/$d
    fi
done

#============ 資料備份 ============#

cp ../usr/share/zoneinfo/Asia/Taipei ../etc/localtime # 更換時區

SLEEP_TIME=600 # sec

while true
do 
    sleep ${SLEEP_TIME} # 服務尚未啟動，等服務啟動後再進行備份，避免備份空資料

    for d in $dir
    do
        cp data/$d.json ${BACKUP_DIR}/$d/$(date +'%Y%m%d%H').json
    done

    echo backup success
done & # 背景執行

#============ 啟動服務 ============#

python api.py