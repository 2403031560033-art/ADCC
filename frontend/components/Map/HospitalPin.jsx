import { Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

// Fix for default icon bug in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

export default function HospitalPin({ hospital }) {
  return (
    <Marker position={[hospital.lat, hospital.lon]}>
      <Popup>
        <div style={{ fontFamily: 'monospace' }}>
          <strong>{hospital.name}</strong> ({hospital.hospital_id})<br />
          Capacity: {hospital.capacity}<br />
          Available Beds: {hospital.available_beds}
        </div>
      </Popup>
    </Marker>
  );
}
