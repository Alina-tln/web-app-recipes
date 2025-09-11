-- create a user for the application
CREATE USER app_user WITH PASSWORD 'app_pass';

-- grant permissions for application
GRANT CONNECT ON DATABASE recipes_db TO app_user;
GRANT USAGE ON SCHEMA users, recipes, translations TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;

-- table permissions for app-user
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;
