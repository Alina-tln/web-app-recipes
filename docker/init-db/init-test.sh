#!/bin/bash
set -e

# =========================================================================
# 0. VARIABLES AND SETTINGS
# =========================================================================

SCHEMAS="recipes users translations"
echo "Initializing test db: $TEST_DB_NAME with user $TEST_DB_USER"

# 1. Generate SQL to create schemas, grant ALL privileges (including USAGE) on the schema itself, and transfer ownership.
SQL_CREATE_SCHEMAS_AND_GRANT=""
for schema in $SCHEMAS; do
    SQL_CREATE_SCHEMAS_AND_GRANT="${SQL_CREATE_SCHEMAS_AND_GRANT}CREATE SCHEMA IF NOT EXISTS $schema;"
    # Grant ALL (which includes USAGE) on the schema to the test user immediately.
    SQL_CREATE_SCHEMAS_AND_GRANT="${SQL_CREATE_SCHEMAS_AND_GRANT}GRANT ALL ON SCHEMA $schema TO $TEST_DB_USER;"
    SQL_CREATE_SCHEMAS_AND_GRANT="${SQL_CREATE_SCHEMAS_AND_GRANT}ALTER SCHEMA $schema OWNER TO $TEST_DB_USER;"
done

# 2. Generate SQL for granting default privileges on FUTURE objects (ALTER DEFAULT PRIVILEGES).
SQL_GRANT_DEFAULT_PRIVILEGES=""
for schema in $SCHEMAS; do
    # Grant default privileges on FUTURE objects (tables, sequences, functions)
    SQL_GRANT_DEFAULT_PRIVILEGES="${SQL_GRANT_DEFAULT_PRIVILEGES}ALTER DEFAULT PRIVILEGES IN SCHEMA $schema GRANT ALL ON TABLES TO $TEST_DB_USER;"
    SQL_GRANT_DEFAULT_PRIVILEGES="${SQL_GRANT_DEFAULT_PRIVILEGES}ALTER DEFAULT PRIVILEGES IN SCHEMA $schema GRANT ALL ON SEQUENCES TO $TEST_DB_USER;"
    SQL_GRANT_DEFAULT_PRIVILEGES="${SQL_GRANT_DEFAULT_PRIVILEGES}ALTER DEFAULT PRIVILEGES IN SCHEMA $schema GRANT ALL ON FUNCTIONS TO $TEST_DB_USER;"
done


# =========================================================================
# 1. CREATING A TEST DATABASE AND USER (TEST ROLE)
# =========================================================================

# Connection to the main db as superuser
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

    DROP USER IF EXISTS $TEST_DB_USER;

    # Create a "strong" role for testing (CREATEDB, CREATEROLE)
    CREATE USER $TEST_DB_USER WITH PASSWORD '$TEST_DB_PASSWORD' CREATEDB CREATEROLE;
    DROP DATABASE IF EXISTS $TEST_DB_NAME;
    CREATE DATABASE $TEST_DB_NAME WITH OWNER $TEST_DB_USER;
    GRANT ALL PRIVILEGES ON DATABASE $TEST_DB_NAME TO $TEST_DB_USER;

EOSQL

echo "Test DB successfully created."

# =========================================================================
# 2. WAITING AND SCHEMA CREATION FUNCTION
# =========================================================================

echo "Waiting 5 seconds for main DB to finalize its initialization by Docker..."
sleep 5 # Addresses main DB startup instability

create_schemas() {
    DB_NAME_TO_APPLY=$1
    echo "Creating schemas and granting privileges for database: $DB_NAME_TO_APPLY"

    # Check if ALTER DEFAULT PRIVILEGES should be granted (only for the test DB)
    SHOULD_GRANT_TEST_USER_RIGHTS=0
    if [ "$DB_NAME_TO_APPLY" == "$TEST_DB_NAME" ]; then
        SHOULD_GRANT_TEST_USER_RIGHTS=1
    fi

    # Connecting to the 'postgres' system database for administrative actions
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL

        \connect $DB_NAME_TO_APPLY;

        # Create schemas, grant ALL on schema (USAGE), and set ownership.
        $SQL_CREATE_SCHEMAS_AND_GRANT

        # Conditional default privilege granting (only for the test DB).
        \if :SHOULD_GRANT_TEST_USER_RIGHTS
            $SQL_GRANT_DEFAULT_PRIVILEGES
        \endif

EOSQL
}

# =========================================================================
# 3. FUNCTION CALLS
# =========================================================================

# 3.1 Create schemas in the main DB for development
create_schemas "$POSTGRES_DB"

# 3.2 Create schemas in the test DB (with full default privileges)
create_schemas "$TEST_DB_NAME"

echo "All schemes were created successfully."