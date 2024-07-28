#!/bin/bash

#============ 複製備份檔 ============#

file=$(ls -1 ${BACKUP_DIR}/sql_backup | sort -r | head -n 1)

if [ -n "$file" ]; then
    cp ${BACKUP_DIR}/sql_backup/$file docker-entrypoint-initdb.d/init.sql
    echo COPY FILE ${BACKUP_DIR}/sql_backup/$file
fi

#============ 資料備份 ============#

TIMESTAMP=$(date +'%Y%m%d%H%M')
SLEEP_TIME=60 # sec

while true 
do
    sleep ${SLEEP_TIME} # 服務尚未啟動，等服務啟動後再進行備份，避免備份空資料

    mysqldump -u root --password=root Hotel > ${BACKUP_DIR}/sql_backup/${TIMESTAMP}.sql

    echo backup success
done & # 背景執行

#============ 啟動服務 ============#

docker-entrypoint.sh mysqld