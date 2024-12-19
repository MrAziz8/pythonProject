BACKUP_DIR="/home/aziz/Downloads/backups/"
FILE_NAME=$BACKUP_DIR`date +%d-%m-%Y-%I-%M-%S`.tar
PGPASSWORD='1' pg_dump -U postgres -h localhost -d lesson_4 -F tar -f $FILE_NAME
