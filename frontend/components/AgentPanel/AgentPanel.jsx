import React from 'react';

const agentColors = {
  coordinator: '#534AB7',
  route: '#378ADD',
  resource: '#BA7517',
  medical: '#1D9E75',
  drone: '#D85A30'
};

export default function AgentPanel({ agentUpdates }) {
  const agents = ['coordinator', 'route', 'resource', 'medical', 'drone'];

  return (
    <div style={{ background: '#0F1E35', border: '1px solid #1E3050', borderRadius: '12px', padding: '1.25rem', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <h3 style={{ color: '#F4F5F7', fontSize: '16px', fontWeight: '500', marginBottom: '1rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Agent Activity Panel</h3>
      <div style={{ flex: 1, overflowY: 'auto', paddingRight: '8px', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {agents.map(agent => {
          const update = agentUpdates[agent];
          const color = agentColors[agent];
          
          return (
            <div key={agent} style={{ display: 'flex', alignItems: 'flex-start', gap: '12px', background: '#0A1628', padding: '1rem', borderRadius: '8px' }}>
              <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: color, marginTop: '4px', flexShrink: 0, boxShadow: update ? `0 0 8px ${color}` : 'none' }}></div>
              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                  <span style={{ color: '#F4F5F7', fontWeight: '500', textTransform: 'capitalize' }}>{agent} Agent</span>
                  {update ? (
                    <span style={{ fontSize: '11px', background: '#1D9E7520', color: '#1D9E75', padding: '2px 8px', borderRadius: '10px' }}>Done</span>
                  ) : (
                    <span style={{ fontSize: '11px', color: '#8B9AB0' }}>Waiting...</span>
                  )}
                </div>
                <div style={{ color: '#8B9AB0', fontSize: '13px', lineHeight: '1.5' }}>
                  {update ? update.reasoning : `Awaiting ${agent} execution...`}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
