import React from 'react';

export default function ReportButton({ onClick, isLive }) {
  return (
    <button
      id="report-incident-btn"
      onClick={onClick}
      style={{
        background: isLive ? '#378ADD' : '#2a6eb5',
        color: '#FFFFFF',
        border: 'none',
        padding: '10px 24px',
        borderRadius: '4px',
        fontWeight: 'bold',
        cursor: 'pointer',
        textTransform: 'uppercase',
        letterSpacing: '0.05em',
        fontSize: '13px',
        transition: 'all 0.3s ease',
        boxShadow: isLive ? '0 0 16px rgba(55,138,221,0.4)' : 'none',
        display: 'flex',
        alignItems: 'center',
        gap: '6px',
        animation: isLive ? 'reportPulse 2.5s infinite' : 'none',
      }}
    >
      <span style={{ fontSize: '15px' }}>📡</span>
      Report Incident
      <style jsx>{`
        @keyframes reportPulse {
          0%, 100% { box-shadow: 0 0 8px rgba(55,138,221,0.3); }
          50% { box-shadow: 0 0 20px rgba(55,138,221,0.6); }
        }
      `}</style>
    </button>
  );
}
