import { useState, useEffect, useRef, useCallback } from 'react';
import { io } from 'socket.io-client';

const INITIAL_STATE = {
  agentUpdates: {},
  timelineEvents: [],
  zones: [],          // ← store zones HERE, not in fullState
  metrics: {
    response_time_reduction: 0,
    delivery_efficiency: 0,
    supplies_delivered: 0,
    lives_impacted: 0,
  },
  isSimulationDone: false,
};

let _socket = null;   // module-level singleton so page.jsx and hook share the same conn

function getSocket() {
  if (!_socket || _socket.disconnected) {
    _socket = io('http://localhost:8000', { transports: ['websocket', 'polling'] });
  }
  return _socket;
}

export function useDisasterData() {
  const [state, setState] = useState(INITIAL_STATE);

  useEffect(() => {
    const socket = getSocket();

    const onReset = () => {
      // Wipe ALL data the moment a new disaster starts
      setState(INITIAL_STATE);
    };

    const onAgentUpdate = (data) => {
      setState(prev => ({
        ...prev,
        agentUpdates: { ...prev.agentUpdates, [data.agent]: data },
      }));
    };

    const onTimelineEvent = (data) => {
      setState(prev => ({
        ...prev,
        timelineEvents: [data, ...prev.timelineEvents],
      }));
    };

    const onStateUpdate = (data) => {
      // REPLACE zones entirely (never accumulate)
      if (data.zones) {
        setState(prev => ({ ...prev, zones: data.zones }));
      }
    };

    const onMetricsUpdate = (data) => {
      setState(prev => ({ ...prev, metrics: data }));
    };

    const onSimulationDone = () => {
      setState(prev => ({ ...prev, isSimulationDone: true }));
    };

    socket.on('simulation_reset',   onReset);
    socket.on('agent_update',       onAgentUpdate);
    socket.on('timeline_event',     onTimelineEvent);
    socket.on('state_update',       onStateUpdate);
    socket.on('metrics_update',     onMetricsUpdate);
    socket.on('simulation_complete', onSimulationDone);

    return () => {
      socket.off('simulation_reset',   onReset);
      socket.off('agent_update',       onAgentUpdate);
      socket.off('timeline_event',     onTimelineEvent);
      socket.off('state_update',       onStateUpdate);
      socket.off('metrics_update',     onMetricsUpdate);
      socket.off('simulation_complete', onSimulationDone);
    };
  }, []);

  return state;
}

// Expose the shared socket for page.jsx to attach its own events
export { getSocket };
