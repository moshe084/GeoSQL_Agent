import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, GeoJSON, useMap } from 'react-leaflet';
import L from 'leaflet';
import { QueryResult } from '../types';
import 'leaflet/dist/leaflet.css';

// Fix Leaflet marker icons issue with webpack
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

// Style function for different geometry types
const geoJsonStyle = (feature: any) => {
  const geometryType = feature?.geometry?.type;

  switch (geometryType) {
    case 'LineString':
    case 'MultiLineString':
      return {
        color: '#3388ff',
        weight: 3,
        opacity: 0.8
      };
    case 'Polygon':
    case 'MultiPolygon':
      return {
        color: '#3388ff',
        weight: 2,
        opacity: 0.8,
        fillColor: '#3388ff',
        fillOpacity: 0.2
      };
    default:
      return {
        color: '#3388ff',
        weight: 2
      };
  }
};

interface MapProps {
  results: QueryResult[];
  resultCount?: number;
  executionTime?: number;
}

// Helper function to extract all points from any geometry type
const extractBounds = (geometry: any): [number, number][] => {
  const points: [number, number][] = [];
  const coords = geometry.coordinates;
  const type = geometry.type;

  const addPoint = (coord: number[]) => {
    if (coord.length >= 2) {
      points.push([coord[1], coord[0]]); // [lat, lng] for Leaflet
    }
  };

  const processCoords = (c: any, depth: number) => {
    if (depth === 0) {
      addPoint(c);
    } else if (Array.isArray(c)) {
      c.forEach((item) => processCoords(item, depth - 1));
    }
  };

  switch (type) {
    case 'Point':
      addPoint(coords);
      break;
    case 'LineString':
      processCoords(coords, 1);
      break;
    case 'Polygon':
      processCoords(coords, 2);
      break;
    case 'MultiPoint':
      processCoords(coords, 1);
      break;
    case 'MultiLineString':
      processCoords(coords, 2);
      break;
    case 'MultiPolygon':
      processCoords(coords, 3);
      break;
  }

  return points;
};

const MapUpdater: React.FC<{ results: QueryResult[] }> = ({ results }) => {
  const map = useMap();

  React.useEffect(() => {
    if (results.length > 0) {
      const allPoints: [number, number][] = [];

      results.forEach(r => {
        const points = extractBounds(r.geojson);
        allPoints.push(...points);
      });

      if (allPoints.length > 0) {
        map.fitBounds(allPoints as any, { padding: [50, 50] });
      }
    }
  }, [results, map]);

  return null;
};

export const Map: React.FC<MapProps> = ({ results, resultCount = 0, executionTime = 0 }) => {
  return (
    <div className="h-full w-full relative">
      <MapContainer
        center={[32.0853, 34.7818]}
        zoom={13}
        className="h-full w-full"
        style={{ background: '#E0F2FE' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | <a href="https://leafletjs.com">Leaflet</a>'
        />
        {results.map((result, idx) => {
          const geometryType = result.geojson.type;

          // Extract properties from result object (all fields except 'geojson')
          const properties = Object.entries(result)
            .filter(([key]) => key !== 'geojson')
            .reduce((acc, [key, value]) => ({ ...acc, [key]: value }), {});

          // For Point geometries, use Markers for better visibility
          if (geometryType === 'Point') {
            const coords = result.geojson.coordinates as any;
            if (coords.length === 2) {
              return (
                <Marker key={idx} position={[coords[1], coords[0]]}>
                  <Popup>
                    <div className="text-sm space-y-1">
                      {Object.entries(properties).map(([key, value]) => (
                        <div key={key}>
                          <strong>{key}:</strong> {String(value)}
                        </div>
                      ))}
                    </div>
                  </Popup>
                </Marker>
              );
            }
          }

          // For LineString, Polygon, and other geometries, use GeoJSON
          const popupContent = Object.entries(properties)
            .map(([key, value]) => `<strong>${key}:</strong> ${String(value)}`)
            .join('<br/>');

          return (
            <GeoJSON
              key={idx}
              data={result.geojson as any}
              style={geoJsonStyle}
              onEachFeature={(_feature, layer) => {
                if (popupContent) {
                  layer.bindPopup(popupContent);
                }
              }}
            />
          );
        })}
        <MapUpdater results={results} />
      </MapContainer>

      {/* Results Info */}
      {resultCount > 0 && (
        <div className="absolute bottom-4 left-4 bg-white bg-opacity-90 rounded-lg shadow-lg px-4 py-2 text-sm z-[1000]">
          <div className="flex items-center space-x-4">
            <span className="text-blue-600 font-semibold">Results: {resultCount}</span>
            <span className="text-gray-600">Execution Time: {executionTime}ms</span>
          </div>
        </div>
      )}
    </div>
  );
};
