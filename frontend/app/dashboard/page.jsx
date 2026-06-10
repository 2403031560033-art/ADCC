'use client';

import dynamic from 'next/dynamic';
import { useState, useEffect } from 'react';
import { useDisasterData, getSocket } from '../../hooks/useDisasterData';
import Header from '../../components/Header/Header';
import KPICard from '../../components/KPI/KPICard';
import AgentPanel from '../../components/AgentPanel/AgentPanel';
import Timeline from '../../components/Timeline/Timeline';

const Map = dynamic(() => import('../../components/Map/Map'), { ssr: false });

const DISASTER_ICONS = {
  flood: '🌊', earthquake: '🌍', landslide: '⛰️', cyclone: '🌀', avalanche: '❄️'
};

const STANDBY = { label: 'Standby — Click to Begin', disaster_type: '', region: '—', emoji: '⚡' };

export default function DashboardPage() {
  const [isLive, setIsLive]               = useState(false);
  const [activeScenario, setActiveScenario] = useState(STANDBY);

  const { agentUpdates, timelineEvents, zones, metrics, isSimulationDone } = useDisasterData();

  // When the backend signals simulation is done → reset the button
  useEffect(() => {
    if (isSimulationDone) setIsLive(false);
  }, [isSimulationDone]);

  // Listen for simulation_reset on the shared socket to update header badge
  useEffect(() => {
    const socket = getSocket();
    const handler = (data) => {
      if (data) {
        setActiveScenario({
          label:         data.label         || 'Operation Active',
          disaster_type: data.disaster_type || '',
          region:        data.region        || '—',
          emoji:         data.emoji         || DISASTER_ICONS[data.disaster_type] || '⚡',
        });
      }
      setIsLive(true);
    };
    socket.on('simulation_reset', handler);
    return () => socket.off('simulation_reset', handler);
  }, []);

  const handleTriggerDisaster = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/disaster/create', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({}),   // backend picks a random scenario
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      // header badge updated by socket event; also set here as immediate fallback
      setActiveScenario({
        label:         data.label         || 'Operation Active',
        disaster_type: data.disaster_type || '',
        region:        data.region        || '—',
        emoji:         data.emoji         || DISASTER_ICONS[data.disaster_type] || '⚡',
      });
      setIsLive(true);
    } catch (err) {
      console.error('Failed to trigger disaster', err);
      setIsLive(false);
    }
  };

  return (
    <div style={{ backgroundColor: '#0A1628', color: '#F4F5F7', minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header onTriggerDisaster={handleTriggerDisaster} isLive={isLive} activeScenario={activeScenario} />

      <div style={{ padding: '2rem', flex: 1, display: 'flex', flexDirection: 'column', gap: '2rem' }}>

        {/* KPI Row */}
        <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
          <KPICard label="Response"   value={metrics.response_time_reduction || 0} unit="%" isActive={isLive} />
          <KPICard label="Efficiency" value={metrics.delivery_efficiency      || 0} unit="%" isActive={isLive} />
          <KPICard label="Supplies"   value={metrics.supplies_delivered       || 0} unit=""  isActive={isLive} />
          <KPICard label="Lives"      value={metrics.lives_impacted           || 0} unit=""  isActive={isLive} />
        </div>

        {/* Map — only zones from the CURRENT simulation */}
        <div style={{ height: '500px', borderRadius: '12px', overflow: 'hidden', border: '1px solid #1E3050' }}>
          <Map zones={zones} />
        </div>

        {/* Bottom Row */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', minHeight: '400px' }}>
          <div style={{ height: '400px' }}>
            <Timeline timelineEvents={timelineEvents} />
          </div>
          <div style={{ height: '400px' }}>
            <AgentPanel agentUpdates={agentUpdates} />
          </div>
        </div>

      </div>

      <style jsx global>{`
        body { margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        @media (max-width: 768px) {
          div[style*="grid-template-columns: 1fr 1fr"] { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </div>
  );
}
