-- Create plans table for Israeli planning data
-- Based on data from Israeli Planning Administration (mimhal hatechnun)

CREATE TABLE IF NOT EXISTS plans (
    id SERIAL PRIMARY KEY,
    pl_number VARCHAR(78),                    -- מספר תכנית
    pl_name TEXT,                             -- שם תכנית
    pl_url TEXT,                              -- קישור לאתר מידע תכנוני
    pl_area_dunam DOUBLE PRECISION,           -- שטח תכנית בדונם
    quantity_delta_120 DOUBLE PRECISION,      -- שינוי מספר יחידות דיור
    station_desc VARCHAR(100),                -- תיאור סטטוס
    internet_short_status VARCHAR(100),       -- שלב תכנוני רצוי
    pl_date_advertise DATE,                   -- תאריך פרסום בעיתונים
    pl_date_8 DATE,                           -- תאריך פרסום ברשומות
    plan_county_name VARCHAR(100),            -- שם יישוב
    pl_landuse_string TEXT,                   -- סוג ייעוד קרקע
    geom GEOMETRY(Polygon, 4326)              -- גיאומטריה של התכנית
);

-- Create spatial index for fast queries
CREATE INDEX idx_plans_geom ON plans USING GIST(geom);

-- Create indexes on commonly queried fields
CREATE INDEX idx_plans_number ON plans(pl_number);
CREATE INDEX idx_plans_status ON plans(station_desc);
CREATE INDEX idx_plans_county ON plans(plan_county_name);
CREATE INDEX idx_plans_landuse ON plans(pl_landuse_string);

-- Add comments for documentation
COMMENT ON TABLE plans IS 'תכניות בניין עיר מממינהל התכנון הישראלי';
COMMENT ON COLUMN plans.pl_number IS 'מספר תכנית';
COMMENT ON COLUMN plans.pl_name IS 'שם תכנית';
COMMENT ON COLUMN plans.pl_url IS 'קישור לאתר מידע תכנוני';
COMMENT ON COLUMN plans.pl_area_dunam IS 'שטח תכנית בדונם';
COMMENT ON COLUMN plans.quantity_delta_120 IS 'שינוי במספר יחידות דיור';
COMMENT ON COLUMN plans.station_desc IS 'תיאור סטטוס התכנית';
COMMENT ON COLUMN plans.internet_short_status IS 'שלב תכנוני נוכחי';
COMMENT ON COLUMN plans.pl_date_advertise IS 'תאריך פרסום בעיתונים';
COMMENT ON COLUMN plans.pl_date_8 IS 'תאריך פרסום ברשומות';
COMMENT ON COLUMN plans.plan_county_name IS 'שם היישוב בו התכנית';
COMMENT ON COLUMN plans.pl_landuse_string IS 'סוג ייעוד הקרקע';
COMMENT ON COLUMN plans.geom IS 'גיאומטריה (פוליגון) של התכנית';
