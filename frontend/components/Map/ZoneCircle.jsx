import { CircleMarker, Popup } from 'react-leaflet';

export default function ZoneCircle({ zone }) {
  let color = '#F4D35A'; // yellow for 1-4
  let radius = 10;

  if (zone.severity >= 8) {
    color = '#E8410A'; // red for 8-10
    radius = 18;
  } else if (zone.severity >= 5) {
    color = '#BA7517'; // orange for 5-7
    radius = 14;
  }

  const dashArray = zone.road_accessible ? null : '5, 5';

  return (
    <CircleMarker
      center={[zone.lat, zone.lon]}
      radius={radius}
      pathOptions={{
        color: zone.road_accessible ? color : '#E8410A',
        fillColor: color,
        fillOpacity: 0.7,
        dashArray: dashArray,
        weight: zone.road_accessible ? 2 : 3
      }}
    >
      <Popup>
        <div style={{ fontFamily: 'monospace' }}>
          <strong>{zone.name}</strong> ({zone.zone_id})<br />
          Severity: {zone.severity}<br />
          Population: {zone.population}<br />
          Road Accessible: {zone.road_accessible ? 'Yes' : 'No'}
        </div>
      </Popup>
    </CircleMarker>
  );
}
