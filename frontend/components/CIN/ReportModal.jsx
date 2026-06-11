'use client';

import React, { useState, useEffect, useCallback } from 'react';

const API_BASE = 'https://adcc-mpf6.onrender.com';

const REPORT_TYPES = [
  { key: 'road_blocked',        label: 'Road Blocked',        emoji: '🔴' },
  { key: 'building_collapsed',  label: 'Building Collapsed',  emoji: '🏚️' },
  { key: 'people_injured',      label: 'People Injured',      emoji: '🟠' },
  { key: 'people_dead',         label: 'People Dead',         emoji: '⚠️' },
  { key: 'request_help',        label: 'Need Rescue',         emoji: '🟡' },
  { key: 'safe_area',           label: 'Safe Area',           emoji: '🟢' },
  { key: 'safe_road',           label: 'Safe Road',           emoji: '🔵' },
];

export default function ReportModal({ isOpen, onClose, onReportSubmitted }) {
  const [form, setForm] = useState({
    latitude: '',
    longitude: '',
    road_blocked: false,
    building_collapsed: false,
    people_injured: false,
    people_dead: false,
    request_help: false,
    safe_area: false,
    safe_road: false,
    description: '',
  });
  const [gpsStatus, setGpsStatus] = useState('idle'); // idle | loading | success | error
  const [submitStatus, setSubmitStatus] = useState('idle'); // idle | loading | success | error
  const [errorMsg, setErrorMsg] = useState('');
  const [validationError, setValidationError] = useState('');

  // Reset form on open
  useEffect(() => {
    if (isOpen) {
      setForm({
        latitude: '', longitude: '',
        road_blocked: false, building_collapsed: false,
        people_injured: false, people_dead: false,
        request_help: false, safe_area: false, safe_road: false,
        description: '',
      });
      setGpsStatus('idle');
      setSubmitStatus('idle');
      setErrorMsg('');
      setValidationError('');
    }
  }, [isOpen]);

  // Escape key to close
  useEffect(() => {
    const handler = (e) => { if (e.key === 'Escape') onClose(); };
    if (isOpen) window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [isOpen, onClose]);

  const handleGPS = useCallback(() => {
    if (!navigator.geolocation) {
      setGpsStatus('error');
      setErrorMsg('Geolocation is not supported by your browser');
      return;
    }
    setGpsStatus('loading');
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setForm(prev => ({
          ...prev,
          latitude: pos.coords.latitude.toFixed(6),
          longitude: pos.coords.longitude.toFixed(6),
        }));
        setGpsStatus('success');
        setErrorMsg('');
      },
      (err) => {
        setGpsStatus('error');
        setErrorMsg(`GPS error: ${err.message}. Enter coordinates manually.`);
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  }, []);

  const toggleFlag = (key) => {
    setForm(prev => ({ ...prev, [key]: !prev[key] }));
    setValidationError('');
  };

  const handleSubmit = async () => {
    // Validate
    if (!form.latitude || !form.longitude) {
      setValidationError('Location is required. Use GPS or enter coordinates manually.');
      return;
    }
    const lat = parseFloat(form.latitude);
    const lon = parseFloat(form.longitude);
    if (isNaN(lat) || lat < -90 || lat > 90) {
      setValidationError('Latitude must be between -90 and 90');
      return;
    }
    if (isNaN(lon) || lon < -180 || lon > 180) {
      setValidationError('Longitude must be between -180 and 180');
      return;
    }
    const hasFlag = REPORT_TYPES.some(t => form[t.key]);
    if (!hasFlag) {
      setValidationError('Select at least one report type');
      return;
    }

    setSubmitStatus('loading');
    setValidationError('');

    try {
      const body = {
        latitude: lat,
        longitude: lon,
        road_blocked: form.road_blocked,
        building_collapsed: form.building_collapsed,
        people_injured: form.people_injured,
        people_dead: form.people_dead,
        request_help: form.request_help,
        safe_area: form.safe_area,
        safe_road: form.safe_road,
        description: form.description || null,
      };

      const res = await fetch(`${API_BASE}/api/reports`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${res.status}`);
      }

      const data = await res.json();
      setSubmitStatus('success');
      if (onReportSubmitted) onReportSubmitted(data);

      // Auto-close after brief success display
      setTimeout(() => onClose(), 1500);
    } catch (err) {
      setSubmitStatus('error');
      setErrorMsg(err.message || 'Failed to submit report');
    }
  };

  if (!isOpen) return null;

  return (
    <div
      id="report-modal-overlay"
      onClick={(e) => { if (e.target.id === 'report-modal-overlay') onClose(); }}
      style={{
        position: 'fixed', inset: 0, zIndex: 9999,
        background: 'rgba(10, 22, 40, 0.85)',
        backdropFilter: 'blur(8px)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        padding: '1rem',
      }}
    >
      <div style={{
        background: '#0F1E35',
        border: '1px solid #1E3050',
        borderRadius: '16px',
        padding: '2rem',
        width: '100%',
        maxWidth: '460px',
        maxHeight: '90vh',
        overflowY: 'auto',
        position: 'relative',
        boxShadow: '0 24px 64px rgba(0,0,0,0.6)',
      }}>
        {/* Close Button */}
        <button
          id="report-modal-close"
          onClick={onClose}
          style={{
            position: 'absolute', top: '16px', right: '16px',
            background: 'none', border: 'none', color: '#8B9AB0',
            fontSize: '20px', cursor: 'pointer', padding: '4px',
            lineHeight: 1,
          }}
        >✕</button>

        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
          <div style={{ fontSize: '32px', marginBottom: '8px' }}>📡</div>
          <h2 style={{ color: '#F4F5F7', fontSize: '20px', fontWeight: '600', margin: 0 }}>
            Community Intelligence
          </h2>
          <p style={{ color: '#8B9AB0', fontSize: '13px', marginTop: '4px' }}>
            Report ground conditions to help emergency teams
          </p>
        </div>

        {/* GPS Button */}
        <button
          id="share-location-btn"
          onClick={handleGPS}
          disabled={gpsStatus === 'loading'}
          style={{
            width: '100%',
            padding: '12px',
            borderRadius: '8px',
            border: '1px solid #1E3050',
            background: gpsStatus === 'success' ? '#1D9E7520' : '#0A1628',
            color: gpsStatus === 'success' ? '#1D9E75' : '#378ADD',
            fontSize: '14px',
            fontWeight: '500',
            cursor: gpsStatus === 'loading' ? 'wait' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            marginBottom: '12px',
            transition: 'all 0.3s ease',
          }}
        >
          {gpsStatus === 'loading' ? '⏳ Getting Location...' :
           gpsStatus === 'success' ? '✅ Location Captured' :
           '📍 Share My Location'}
        </button>

        {/* Lat/Lon display */}
        <div style={{ display: 'flex', gap: '8px', marginBottom: '1.25rem' }}>
          <input
            id="report-latitude"
            type="text"
            placeholder="Latitude"
            value={form.latitude}
            onChange={e => setForm(prev => ({ ...prev, latitude: e.target.value }))}
            style={{
              flex: 1, padding: '10px 12px', borderRadius: '8px',
              border: '1px solid #1E3050', background: '#0A1628',
              color: '#F4F5F7', fontSize: '13px', fontFamily: 'monospace',
              outline: 'none',
            }}
          />
          <input
            id="report-longitude"
            type="text"
            placeholder="Longitude"
            value={form.longitude}
            onChange={e => setForm(prev => ({ ...prev, longitude: e.target.value }))}
            style={{
              flex: 1, padding: '10px 12px', borderRadius: '8px',
              border: '1px solid #1E3050', background: '#0A1628',
              color: '#F4F5F7', fontSize: '13px', fontFamily: 'monospace',
              outline: 'none',
            }}
          />
        </div>

        {/* Report Type Checkboxes */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginBottom: '1.25rem' }}>
          {REPORT_TYPES.map(({ key, label, emoji }) => (
            <label
              key={key}
              id={`report-type-${key}`}
              style={{
                display: 'flex', alignItems: 'center', gap: '10px',
                padding: '10px 12px', borderRadius: '8px',
                border: `1px solid ${form[key] ? '#378ADD' : '#1E3050'}`,
                background: form[key] ? '#378ADD15' : '#0A1628',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
              }}
            >
              <input
                type="checkbox"
                checked={form[key]}
                onChange={() => toggleFlag(key)}
                style={{ display: 'none' }}
              />
              <span style={{
                width: '20px', height: '20px', borderRadius: '4px',
                border: `2px solid ${form[key] ? '#378ADD' : '#2C436B'}`,
                background: form[key] ? '#378ADD' : 'transparent',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '12px', color: '#fff', flexShrink: 0,
                transition: 'all 0.2s ease',
              }}>
                {form[key] && '✓'}
              </span>
              <span style={{ fontSize: '16px' }}>{emoji}</span>
              <span style={{ color: '#F4F5F7', fontSize: '14px' }}>{label}</span>
            </label>
          ))}
        </div>

        {/* Description */}
        <textarea
          id="report-description"
          placeholder="Describe the situation (optional, max 1000 chars)..."
          value={form.description}
          onChange={e => setForm(prev => ({ ...prev, description: e.target.value.slice(0, 1000) }))}
          rows={3}
          style={{
            width: '100%', padding: '12px', borderRadius: '8px',
            border: '1px solid #1E3050', background: '#0A1628',
            color: '#F4F5F7', fontSize: '13px', resize: 'vertical',
            outline: 'none', fontFamily: 'inherit',
            marginBottom: '4px', boxSizing: 'border-box',
          }}
        />
        <div style={{ fontSize: '11px', color: '#556070', textAlign: 'right', marginBottom: '1rem' }}>
          {form.description.length}/1000
        </div>

        {/* Validation Error */}
        {validationError && (
          <div style={{
            background: '#E8410A15', border: '1px solid #E8410A40',
            borderRadius: '8px', padding: '10px 14px',
            color: '#E8410A', fontSize: '13px', marginBottom: '1rem',
          }}>
            ⚠️ {validationError}
          </div>
        )}

        {/* Submit Error */}
        {submitStatus === 'error' && (
          <div style={{
            background: '#E8410A15', border: '1px solid #E8410A40',
            borderRadius: '8px', padding: '10px 14px',
            color: '#E8410A', fontSize: '13px', marginBottom: '1rem',
          }}>
            ❌ {errorMsg}
          </div>
        )}

        {/* Success Banner */}
        {submitStatus === 'success' && (
          <div style={{
            background: '#1D9E7520', border: '1px solid #1D9E7540',
            borderRadius: '8px', padding: '14px',
            color: '#1D9E75', fontSize: '14px', fontWeight: '500',
            textAlign: 'center', marginBottom: '1rem',
          }}>
            ✅ Report submitted successfully!
          </div>
        )}

        {/* Submit Button */}
        <button
          id="submit-report-btn"
          onClick={handleSubmit}
          disabled={submitStatus === 'loading' || submitStatus === 'success'}
          style={{
            width: '100%', padding: '14px',
            borderRadius: '8px', border: 'none',
            background: submitStatus === 'success' ? '#1D9E75' :
                         submitStatus === 'loading' ? '#2a6eb5' : '#378ADD',
            color: '#FFFFFF',
            fontSize: '15px', fontWeight: '600',
            cursor: submitStatus === 'loading' ? 'wait' : 'pointer',
            textTransform: 'uppercase',
            letterSpacing: '0.06em',
            transition: 'all 0.3s ease',
            boxShadow: submitStatus === 'idle' ? '0 4px 16px rgba(55,138,221,0.3)' : 'none',
          }}
        >
          {submitStatus === 'loading' ? '⏳ Submitting...' :
           submitStatus === 'success' ? '✅ Submitted!' :
           'Submit Report'}
        </button>
      </div>
    </div>
  );
}
