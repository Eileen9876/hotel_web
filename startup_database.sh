#!/bin/bash

#============ 複製備份檔 ============#

if [ -d "${BACKUP_DIR}/sql_backup" ]; then
    # 資料夾存在，複製最新的備份檔，備份檔以創建日期命名 YYYYmmddHH

    file=$(ls -1 ${BACKUP_DIR}/sql_backup | sort -r | head -n 1)

    if [ -n "$file" ]; then
        cp ${BACKUP_DIR}/sql_backup/$file docker-entrypoint-initdb.d/init.sql
        echo COPY FILE ${BACKUP_DIR}/sql_backup/$file
    fi
else
    # 資料夾不存在，創建資料夾
    
    mkdir ${BACKUP_DIR}/sql_backup
fi

#============ 資料備份 ============#

cp /usr/share/zoneinfo/Asia/Taipei /etc/localtime # 更換時區

SLEEP_TIME=600 # sec

while true 
do
    sleep ${SLEEP_TIME} # 服務尚未啟動，等服務啟動後再進行備份，避免備份空資料

    mysqldump -u root --password=root Hotel > ${BACKUP_DIR}/sql_backup/$(date +'%Y%m%d%H').sql

    echo backup success
done & # 背景執行

#============ 啟動服務 ============#

docker-entrypoint.sh mysqld