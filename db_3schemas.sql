CREATE SCHEMA users;

CREATE TABLE users.users (
                             id BIGSERIAL PRIMARY KEY,
                             email TEXT UNIQUE NOT NULL,
                             password_hash BYTEA,
                             oauth_id TEXT UNIQUE,
                             provider_name TEXT,
                             is_verified BOOLEAN NOT NULL DEFAULT FALSE,
                             created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE users.groups (
                              id BIGSERIAL PRIMARY KEY,
                              group_name TEXT UNIQUE NOT NULL,
                              description TEXT
);

CREATE TABLE users.user_groups (
                                   user_id BIGINT NOT NULL REFERENCES users.users(id) ON DELETE CASCADE,
                                   group_id BIGINT NOT NULL REFERENCES users.groups(id) ON DELETE CASCADE,
                                   PRIMARY KEY (user_id, group_id)
);

CREATE SCHEMA recipes;

CREATE TABLE recipes.ingredients (
                                     id BIGSERIAL PRIMARY KEY,
                                     common_name TEXT UNIQUE NOT NULL
);

CREATE TABLE recipes.ingredient_categories (
                                               id BIGSERIAL PRIMARY KEY,
                                               category_name TEXT UNIQUE NOT NULL
);

CREATE TABLE recipes.ingredient_category_mapping (
                                                     ingredient_id BIGINT NOT NULL REFERENCES recipes.ingredients(id) ON DELETE CASCADE,
                                                     category_id BIGINT NOT NULL REFERENCES recipes.ingredient_categories(id) ON DELETE CASCADE,
                                                     PRIMARY KEY (ingredient_id, category_id)
);

CREATE TABLE recipes.recipes (
                                 id BIGSERIAL PRIMARY KEY,
                                 author_id BIGINT NOT NULL REFERENCES users.users(id) ON DELETE CASCADE,
                                 cooking_time_minutes INT,
                                 image_url TEXT,
                                 created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                                 updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE recipes.recipe_ingredients (
                                            recipe_id BIGINT NOT NULL REFERENCES recipes.recipes(id) ON DELETE CASCADE,
                                            ingredient_id BIGINT NOT NULL REFERENCES recipes.ingredients(id) ON DELETE CASCADE,
                                            quantity DECIMAL,
                                            unit TEXT,
                                            language_code NOT NULL REFERENCES translations.languages(id),
                                            PRIMARY KEY (recipe_id, ingredient_id, language_code)
);

CREATE TABLE recipes.user_recipes (
                                      id BIGSERIAL PRIMARY KEY,
                                      base_recipe_id BIGINT NOT NULL REFERENCES recipes.recipes(id) ON DELETE CASCADE,
                                      user_id BIGINT NOT NULL REFERENCES users.users(id) ON DELETE CASCADE,
                                      language_code NOT NULL REFERENCES translations.languages(id),
                                      title TEXT NOT NULL,
                                      description TEXT,
                                      instructions TEXT,
                                      UNIQUE (user_id, base_recipe_id, language_code)
);

CREATE TABLE recipes.user_recipe_ingredients (
                                                 user_recipe_id BIGINT NOT NULL REFERENCES recipes.user_recipes(id) ON DELETE CASCADE,
                                                 ingredient_id BIGINT NOT NULL REFERENCES recipes.ingredients(id) ON DELETE CASCADE,
                                                 quantity DECIMAL,
                                                 unit TEXT,
                                                 language_code NOT NULL REFERENCES translations.languages(id),
                                                 UNIQUE (user_recipe_id, ingredient_id, language_code)
);

CREATE SCHEMA translations;

CREATE TABLE translations.languages (
                                        id BIGSERIAL PRIMARY KEY,
                                        language_code VARCHAR(5) UNIQUE NOT NULL,
                                        language_name TEXT UNIQUE NOT NULL
);

CREATE TABLE translations.ingredient_translations (
                                                      id BIGSERIAL PRIMARY KEY,
                                                      ingredient_id BIGINT NOT NULL REFERENCES recipes.ingredients(id) ON DELETE CASCADE,
                                                      language_code BIGINT NOT NULL REFERENCES translations.languages(id),
                                                      name TEXT NOT NULL,
                                                      UNIQUE (ingredient_id, language_code)
);

CREATE TABLE translations.recipe_translations (
                                                  id BIGSERIAL PRIMARY KEY,
                                                  recipe_id BIGINT NOT NULL REFERENCES recipes.recipes(id) ON DELETE CASCADE,
                                                  language_code BIGINT NOT NULL REFERENCES translations.languages(id),
                                                  title TEXT NOT NULL,
                                                  description TEXT,
                                                  instructions TEXT,
                                                  UNIQUE (recipe_id, language_code)
);

CREATE INDEX idx_recipe_translations_id_lang ON translations.recipe_translations (recipe_id, language_code);
CREATE INDEX idx_user_recipes_user_id ON recipes.user_recipes (user_id, base_recipe_id);




--Create test_user and test_db for tests
CREATE USER test_user WITH PASSWORD 'le8cyxoM';
CREATE DATABASE test_db OWNER test_user;
