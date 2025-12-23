#!/usr/bin/env python3
"""
Import Israeli planning data from Plans.json to PostGIS database
יבוא נתוני תכניות בניין עיר מממינהל התכנון לבסיס נתונים
"""

import json
import psycopg2
from psycopg2.extras import execute_batch
from shapely.geometry import shape, Polygon
from shapely import wkt
import sys
from datetime import datetime

# Database connection parameters
DB_PARAMS = {
    'dbname': 'geospatial',
    'user': 'geouser',
    'password': 'geopass',
    'host': 'localhost',
    'port': '5433'  # Changed port to match docker-compose.yml
}

def load_json_data(json_file):
    """Load and parse the Plans.json file"""
    print(f"[INFO] Loading {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"[SUCCESS] Loaded {len(data.get('features', []))} features")
    return data

def convert_geometry(geometry_data):
    """Convert ESRI JSON geometry to WKT format for PostGIS"""
    try:
        if not geometry_data:
            return None

        # ESRI JSON uses 'rings' for polygons, convert to GeoJSON format
        if 'rings' in geometry_data:
            # Convert ESRI JSON polygon to GeoJSON polygon
            geojson_geom = {
                "type": "Polygon",
                "coordinates": geometry_data['rings']
            }
            geom = shape(geojson_geom)
        else:
            # Try standard GeoJSON format
            geom = shape(geometry_data)

        # Convert to WKT
        return geom.wkt
    except Exception as e:
        print(f"[WARNING] Error converting geometry: {e}")
        return None

def convert_timestamp_to_date(timestamp):
    """Convert Unix timestamp (milliseconds) to date object"""
    try:
        if timestamp is None:
            return None
        # ESRI timestamps are in milliseconds since epoch
        return datetime.fromtimestamp(timestamp / 1000).date()
    except:
        return None

def import_plans(json_data):
    """Import plans data into PostGIS database"""

    conn = None
    try:
        # Connect to database
        print("[INFO] Connecting to PostGIS database...")
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        # Check if table exists and is empty
        cursor.execute("SELECT COUNT(*) FROM plans")
        existing_count = cursor.fetchone()[0]
        if existing_count > 0:
            print(f"[WARNING] Table 'plans' already contains {existing_count} records.")
            user_input = input("Do you want to clear and re-import? (yes/no): ")
            if user_input.lower() != 'yes':
                print("[INFO] Import cancelled by user")
                return
            cursor.execute("TRUNCATE TABLE plans")
            conn.commit()
            print("[INFO] Table cleared, ready for import")
        else:
            print("[INFO] Table 'plans' is empty, ready for import")

        # Prepare data for batch insert
        features = json_data.get('features', [])
        print(f"[INFO] Preparing to import {len(features)} plans...")

        insert_query = """
        INSERT INTO plans (
            pl_number, pl_name, pl_url, pl_area_dunam, quantity_delta_120,
            station_desc, internet_short_status, pl_date_advertise, pl_date_8,
            plan_county_name, pl_landuse_string, geom
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326)
        )
        """

        # Convert data to tuples for batch insert
        batch_data = []
        skipped = 0

        for i, feature in enumerate(features, 1):
            attrs = feature.get('attributes', {})
            geometry = feature.get('geometry')

            # Convert geometry
            if geometry:
                geom_wkt = convert_geometry(geometry)
                if not geom_wkt:
                    skipped += 1
                    continue
            else:
                skipped += 1
                continue

            # Prepare row data
            row = (
                attrs.get('pl_number'),
                attrs.get('pl_name'),
                attrs.get('pl_url'),
                attrs.get('pl_area_dunam'),
                attrs.get('quantity_delta_120'),
                attrs.get('station_desc'),
                attrs.get('internet_short_status'),
                convert_timestamp_to_date(attrs.get('pl_date_advertise')),
                convert_timestamp_to_date(attrs.get('pl_date_8')),
                attrs.get('plan_county_name'),
                attrs.get('pl_landuse_string'),
                geom_wkt
            )

            batch_data.append(row)

            # Show progress every 100 features
            if i % 100 == 0:
                print(f"   Processing... {i}/{len(features)} ({(i/len(features)*100):.1f}%)")

        # Execute batch insert
        print(f"[INFO] Inserting {len(batch_data)} plans into database...")
        execute_batch(cursor, insert_query, batch_data, page_size=100)
        conn.commit()

        # Get count
        cursor.execute("SELECT COUNT(*) FROM plans")
        count = cursor.fetchone()[0]

        print("="*60)
        print("[SUCCESS] IMPORT COMPLETED SUCCESSFULLY!")
        print(f"[INFO] Total plans imported: {count}")
        print(f"[WARNING] Skipped (no geometry): {skipped}")
        print("="*60)

        # Show some statistics
        cursor.execute("""
            SELECT
                station_desc,
                COUNT(*) as count
            FROM plans
            WHERE station_desc IS NOT NULL
            GROUP BY station_desc
            ORDER BY count DESC
            LIMIT 5
        """)

        print("\n[INFO] Top 5 plan statuses:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]} plans")

    except Exception as e:
        print("[ERROR] Import failed - see error details")
        print(f"[ERROR] Error type: {type(e).__name__}")
        if conn:
            conn.rollback()
        sys.exit(1)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("\n[INFO] Database connection closed")

if __name__ == "__main__":
    # Load JSON data
    json_data = load_json_data('Plans.json')

    # Import to PostGIS
    import_plans(json_data)

    print("\n[SUCCESS] Done! You can now query the 'plans' table")
    print("[INFO] Example query: SELECT pl_name, station_desc FROM plans LIMIT 5;")
