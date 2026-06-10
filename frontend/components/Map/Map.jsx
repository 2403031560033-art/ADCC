'use client';

import { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Severity → colour mapping
function zoneColor(severity) {
  if (severity >= 8) return '#E8410A';   // critical – red-orange
  if (severity >= 5) return '#F5A623';   // moderate – amber
  return '#1D9E75';                       // stable – green
}

// Inner component that can access the Leaflet map instance
function ZoneLayer({ zones }) {
  const map = useMap();
  const layerRef = useRef(null);

  useEffect(() => {
    // Remove old layer completely before adding new ones
    if (layerRef.current) {
      layerRef.current.clearLayers();
    } else {
      layerRef.current = L.layerGroup().addTo(map);
    }

    if (!zones || zones.length === 0) return;

    zones.forEach(z => {
      const radius = 5000 + z.severity * 2500;
      const circle = L.circle([z.lat, z.lon], {
        radius,
        color:       zoneColor(z.severity),
        fillColor:   zoneColor(z.severity),
        fillOpacity: 0.45,
        weight:      1.5,
      });
      circle.bindTooltip(
        `<b>${z.name}</b><br/>Severity: ${z.severity}/10<br/>Pop: ${z.population.toLocaleString()}<br/>Road: ${z.road_accessible ? '✅' : '❌'}`,
        { permanent: false, direction: 'top' }
      );
      layerRef.current.addLayer(circle);
    });

    // Auto-fit map to current zones
    if (zones.length > 0) {
      const bounds = L.latLngBounds(zones.map(z => [z.lat, z.lon]));
      map.fitBounds(bounds, { padding: [40, 40], maxZoom: 9 });
    }
  }, [zones, map]);

  return null;
}

export default function Map({ zones = [] }) {
  return (
    <MapContainer
      center={[26.5, 82.0]}
      zoom={5}
      style={{ height: '100%', width: '100%', minHeight: '400px', borderRadius: '12px' }}
    >
      <TileLayer
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        attribution="&copy; CARTO"
      />
      <ZoneLayer zones={zones} />
    </MapContainer>
  );
}
