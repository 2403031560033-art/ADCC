import React from 'react';

export default function Header({ onTriggerDisaster, isLive, activeScenario, extraActions }) {
  const scenario = activeScenario || { label: 'Standby', region: '—', emoji: '⚡', disaster_type: 'system' };

  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem 2rem', background: '#0F1E35', borderBottom: '1px solid #1E3050' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <h1 style={{ fontFamily: 'monospace', fontSize: '24px', fontWeight: 'bold', color: '#F4F5F7', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
          ADCC
          {isLive && <span style={{ width: '8px', height: '8px', background: '#E8410A', borderRadius: '50%', boxShadow: '0 0 8px #E8410A', animation: 'pulse 1.2s infinite' }}></span>}
        </h1>
        <div style={{ background: '#1E3050', padding: '4px 14px', borderRadius: '16px', fontSize: '12px', color: '#8B9AB0', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span>{scenario.emoji}</span>
          <span style={{ color: '#C0CCD8', fontWeight: '500' }}>{scenario.label}</span>
          <span style={{ color: '#556070' }}>·</span>
          <span>{scenario.region}</span>
          {scenario.disaster_type && scenario.disaster_type !== 'system' && (
            <>
              <span style={{ color: '#556070' }}>·</span>
              <span style={{ textTransform: 'capitalize' }}>{scenario.disaster_type}</span>
            </>
          )}
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        {extraActions}
        <button 
          onClick={onTriggerDisaster}
          style={{ 
            background: isLive ? '#b33006' : '#E8410A', 
            color: '#FFFFFF', 
            border: 'none', 
            padding: '10px 28px', 
            borderRadius: '4px', 
            fontWeight: 'bold',
            cursor: 'pointer',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            fontSize: '13px',
            transition: 'background 0.3s ease',
            boxShadow: isLive ? '0 0 16px rgba(232,65,10,0.5)' : 'none'
          }}
        >
          {isLive ? '⚡ Simulation Running...' : '▶ Trigger Disaster'}
        </button>
      </div>
      <style jsx global>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.4; transform: scale(1.4); }
        }
      `}</style>
    </div>
  );
}
