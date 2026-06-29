#!/bin/bash
set -e

# --- Configuration ---
NAMESPACE="url-shortener"
DB_NAME="urlshortener"
DB_USER="root"
DB_PASSWORD="secret123"
BACKUP_DIR="backups"

# --- Create backup directory if it doesn't exist ---
mkdir -p "$BACKUP_DIR"

# --- Build a filename with the current date ---
DATE=$(date +%Y-%m-%d)
BACKUP_FILE="$BACKUP_DIR/backup-$DATE.sql"

# --- Find the MySQL pod name ---
MYSQL_POD=$(kubectl get pods -n "$NAMESPACE" -l app=mysql -o jsonpath="{.items[0].metadata.name}")

echo "Backing up database '$DB_NAME' from pod '$MYSQL_POD'..."

# --- Run mysqldump inside the pod and save the output locally ---
kubectl exec -n "$NAMESPACE" "$MYSQL_POD" -- \
  mysqldump -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" > "$BACKUP_FILE"

echo "Backup saved to $BACKUP_FILE"
