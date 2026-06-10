import React from 'react';

export default function KPICard({ label, value, unit, isActive }) {
  return (
    <div style={{ background: '#0F1E35', border: '1px solid #1E3050', borderRadius: '12px', padding: '1.5rem', flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ fontSize: '36px', fontWeight: 'bold', color: isActive ? '#1D9E75' : '#F4F5F7', marginBottom: '4px' }}>
        {value}{unit}
      </div>
      <div style={{ fontSize: '13px', color: '#8B9AB0', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
        {label}
      </div>
    </div>
  );
}
