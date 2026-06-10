import React from 'react';

const agentColors = {
  coordinator: '#534AB7',
  route: '#378ADD',
  resource: '#BA7517',
  medical: '#1D9E75',
  drone: '#D85A30',
  system: '#8B9AB0'
};

export default function Timeline({ timelineEvents }) {
  return (
    <div style={{ background: '#0F1E35', border: '1px solid #1E3050', borderRadius: '12px', padding: '1.25rem', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <h3 style={{ color: '#F4F5F7', fontSize: '16px', fontWeight: '500', marginBottom: '1rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Timeline</h3>
      <div style={{ flex: 1, overflowY: 'auto', paddingRight: '8px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {timelineEvents.length === 0 ? (
          <div style={{ color: '#8B9AB0', fontSize: '13px', textAlign: 'center', marginTop: '2rem' }}>No events yet. Trigger disaster to begin.</div>
        ) : (
          timelineEvents.map((evt, idx) => {
            const color = agentColors[evt.agent] || '#8B9AB0';
            const time = new Date(evt.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            
            return (
              <div key={evt.event_id || idx} style={{ display: 'flex', gap: '12px', position: 'relative' }}>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: color, zIndex: 2 }}></div>
                  {idx !== timelineEvents.length - 1 && (
                    <div style={{ width: '2px', background: '#1E3050', flex: 1, marginTop: '4px', marginBottom: '-16px' }}></div>
                  )}
                </div>
                <div style={{ paddingBottom: '1rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                    <span style={{ color: '#8B9AB0', fontSize: '12px', fontFamily: 'monospace' }}>{time}</span>
                    <span style={{ background: `${color}20`, color: color, fontSize: '11px', padding: '2px 6px', borderRadius: '4px', textTransform: 'uppercase' }}>{evt.event_type}</span>
                  </div>
                  <div style={{ color: '#F4F5F7', fontSize: '14px', lineHeight: '1.5' }}>
                    {evt.description}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
