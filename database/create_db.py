import os
import psycopg2
from dotenv import load_dotenv

load_dotenv("../env/dev.env")

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS")
)

conn.autocommit = True
cur = conn.cursor()

try:
    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS nutrition;
        SET search_path TO nutrition;
        
        CREATE TABLE IF NOT EXISTS recipes (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            description TEXT,
            instructions TEXT,
            total_time_minutes INTEGER,
            servings INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    
        CREATE TABLE IF NOT EXISTS ingredients (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            category VARCHAR,
            calories_per_100g NUMERIC
        );
    
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
            id SERIAL PRIMARY KEY,
            recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
            ingredient_id BIGINT NOT NULL REFERENCES ingredients(id) ON DELETE RESTRICT,
            quantity NUMERIC,
            quantity_unit VARCHAR,
            grams NUMERIC
        );
    
        CREATE TABLE IF NOT EXISTS nutrients (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            type VARCHAR CHECK (type IN ('macro', 'micro', 'other')),
            unit VARCHAR NOT NULL,
            recommended_amount_per_kg NUMERIC
        );
    
        CREATE TABLE IF NOT EXISTS ingredient_nutrients (
            id SERIAL PRIMARY KEY,
            ingredient_id BIGINT NOT NULL REFERENCES ingredients(id) ON DELETE CASCADE,
            nutrient_id INTEGER NOT NULL REFERENCES nutrients(id) ON DELETE RESTRICT,
            amount_per_100g NUMERIC NOT NULL
        );
    
        CREATE TABLE IF NOT EXISTS nutrient_recommended_intake (
            id SERIAL PRIMARY KEY,
            nutrient_id INTEGER NOT NULL REFERENCES nutrients(id) ON DELETE CASCADE,
            sex VARCHAR CHECK (sex IN ('male', 'female', 'any')),
            age_min INTEGER,
            age_max INTEGER,
            recommended_amount NUMERIC NOT NULL
        );
    
        CREATE TABLE IF NOT EXISTS people (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            surname VARCHAR,
            age INTEGER,
            sex VARCHAR CHECK (sex IN ('male', 'female', 'other')),
            weight_kg NUMERIC
        );
    
        CREATE TABLE IF NOT EXISTS peoples_disliked_ingredients (
            id SERIAL PRIMARY KEY,
            person_id INTEGER NOT NULL REFERENCES people(id) ON DELETE CASCADE,
            ingredient_id BIGINT NOT NULL REFERENCES ingredients(id) ON DELETE RESTRICT
        );
        
        CREATE TABLE IF NOT EXISTS peoples_disliked_categories (
            id SERIAL PRIMARY KEY,
            person_id INTEGER NOT NULL REFERENCES people(id) ON DELETE CASCADE,
            category VARCHAR NOT NULL
        );
    """)

    print("Database schema created successfully.")
except Exception as e:
    print(f"Database schema not created, ERROR: {e}")

cur.close()
conn.close()
