#!/bin/bash
set -o allexport
source .env
set +o allexport

# Tạo MD5 hash cho password
HASH=$(echo -n "${DB_PASSWORD}${DB_USER}" | md5sum | awk '{print $1}')
HASH="md5${HASH}"

# Export thêm biến
export DB_PASSWORD_HASH=$HASH
export POSTGRES_HOST=stock-predict-postgres

# Sinh 2 file thật
envsubst < pgbouncer.ini.template > pgbouncer.ini
envsubst < userlist.txt.template > userlist.txt

echo "✅ Generated pgbouncer.ini and userlist.txt successfully!"
