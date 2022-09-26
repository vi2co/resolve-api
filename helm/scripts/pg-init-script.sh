#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE TABLE lookup (id serial primary key, addresses VARCHAR(255), client_ip VARCHAR(32), created_at VARCHAR(32), domain_name VARCHAR (50));
EOSQL
