-- Sample data for Tel Aviv area
-- Coordinates are in SRID 4326 (WGS84 - longitude, latitude)

-- Insert sample cafes
INSERT INTO cafes (name, address, geom) VALUES
('Cafe Nero', 'Rothschild Blvd 12', ST_GeomFromText('POINT(34.7714 32.0634)', 4326)),
('Coffee Bar', 'Dizengoff St 50', ST_GeomFromText('POINT(34.7745 32.0753)', 4326)),
('Aroma', 'Ibn Gabirol St 71', ST_GeomFromText('POINT(34.7833 32.0853)', 4326)),
('Cafe Joe', 'Allenby St 45', ST_GeomFromText('POINT(34.7698 32.0678)', 4326)),
('Landwer Cafe', 'Ben Yehuda St 130', ST_GeomFromText('POINT(34.7734 32.0823)', 4326)),
('Cafe Xoho', 'Rothschild Blvd 43', ST_GeomFromText('POINT(34.7720 32.0640)', 4326)),
('Espresso Bar', 'Dizengoff St 121', ST_GeomFromText('POINT(34.7750 32.0790)', 4326)),
('Benedict', 'Rothschild Blvd 29', ST_GeomFromText('POINT(34.7718 32.0636)', 4326)),
('Cafe Noir', 'Ahad Ha''Am St 18', ST_GeomFromText('POINT(34.7685 32.0615)', 4326)),
('Arcaffe', 'Dizengoff Center', ST_GeomFromText('POINT(34.7746 32.0785)', 4326)),
('Cafelix', 'Ibn Gabirol St 41', ST_GeomFromText('POINT(34.7825 32.0825)', 4326)),
('Cafe Bialik', 'Bialik St 9', ST_GeomFromText('POINT(34.7703 32.0723)', 4326)),
('Black Coffee', 'Allenby St 89', ST_GeomFromText('POINT(34.7710 32.0695)', 4326)),
('Cafe Europa', 'Ben Yehuda St 52', ST_GeomFromText('POINT(34.7728 32.0798)', 4326)),
('Urban Coffee', 'Nahalat Binyamin St 18', ST_GeomFromText('POINT(34.7690 32.0693)', 4326));

-- Insert sample parks
INSERT INTO parks (name, area, geom) VALUES
('Meir Park',
 38500,
 ST_GeomFromText('POLYGON((34.7810 32.0825, 34.7835 32.0825, 34.7835 32.0800, 34.7810 32.0800, 34.7810 32.0825))', 4326)),

('Rothschild Park',
 12000,
 ST_GeomFromText('POLYGON((34.7710 32.0630, 34.7730 32.0630, 34.7730 32.0615, 34.7710 32.0615, 34.7710 32.0630))', 4326)),

('Independence Park',
 45000,
 ST_GeomFromText('POLYGON((34.7685 32.0735, 34.7720 32.0735, 34.7720 32.0705, 34.7685 32.0705, 34.7685 32.0735))', 4326)),

('Yarkon Park North',
 185000,
 ST_GeomFromText('POLYGON((34.7850 32.0980, 34.8050 32.0980, 34.8050 32.0850, 34.7850 32.0850, 34.7850 32.0980))', 4326)),

('Dizengoff Square',
 3200,
 ST_GeomFromText('POLYGON((34.7744 32.0773, 34.7754 32.0773, 34.7754 32.0763, 34.7744 32.0763, 34.7744 32.0773))', 4326)),

('London Garden',
 8500,
 ST_GeomFromText('POLYGON((34.7695 32.0665, 34.7715 32.0665, 34.7715 32.0650, 34.7695 32.0650, 34.7695 32.0665))', 4326)),

('Charles Clore Park',
 115000,
 ST_GeomFromText('POLYGON((34.7580 32.0600, 34.7680 32.0600, 34.7680 32.0520, 34.7580 32.0520, 34.7580 32.0600))', 4326));

-- Insert sample roads
INSERT INTO roads (name, road_type, geom) VALUES
('Rothschild Boulevard',
 'main',
 ST_GeomFromText('LINESTRING(34.7710 32.0610, 34.7715 32.0625, 34.7720 32.0640, 34.7725 32.0655)', 4326)),

('Dizengoff Street',
 'main',
 ST_GeomFromText('LINESTRING(34.7745 32.0750, 34.7746 32.0765, 34.7748 32.0780, 34.7750 32.0795)', 4326)),

('Ibn Gabirol Street',
 'main',
 ST_GeomFromText('LINESTRING(34.7825 32.0815, 34.7828 32.0830, 34.7830 32.0845, 34.7833 32.0860)', 4326)),

('Ben Yehuda Street',
 'secondary',
 ST_GeomFromText('LINESTRING(34.7728 32.0795, 34.7730 32.0805, 34.7732 32.0815, 34.7734 32.0825)', 4326)),

('Allenby Street',
 'secondary',
 ST_GeomFromText('LINESTRING(34.7695 32.0670, 34.7700 32.0680, 34.7705 32.0690, 34.7710 32.0700)', 4326)),

('Beach Promenade',
 'pedestrian',
 ST_GeomFromText('LINESTRING(34.7550 32.0600, 34.7570 32.0650, 34.7590 32.0700, 34.7610 32.0750)', 4326));

-- Verify data
SELECT 'Cafes inserted: ' || COUNT(*) FROM cafes;
SELECT 'Parks inserted: ' || COUNT(*) FROM parks;
SELECT 'Roads inserted: ' || COUNT(*) FROM roads;
