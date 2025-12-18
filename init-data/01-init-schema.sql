-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create cafes table
CREATE TABLE cafes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    geom GEOMETRY(Point, 4326)
);

-- Create parks table
CREATE TABLE parks (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    area FLOAT,
    geom GEOMETRY(Polygon, 4326)
);

-- Create roads table
CREATE TABLE roads (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    road_type TEXT,
    geom GEOMETRY(LineString, 4326)
);

-- Create spatial indexes
CREATE INDEX idx_cafes_geom ON cafes USING GIST(geom);
CREATE INDEX idx_parks_geom ON parks USING GIST(geom);
CREATE INDEX idx_roads_geom ON roads USING GIST(geom);
