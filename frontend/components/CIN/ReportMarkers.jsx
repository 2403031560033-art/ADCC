'use client';

import { useEffect, useRef } from 'react';
import { useMap } from 'react-leaflet';
import L from 'leaflet';

/**
 * Report type → marker color mapping.
 * Priority order: first matching flag determines the marker color.
 */
const REPORT_COLORS = [
  { key: 'road_blocked',       color: '#E8410A', label: 'Road Blocked' },
  { key: 'building_collapsed', color: '#E8410A', label: 'Building Collapsed' },
  { key: 'people_dead',        color: '#FF3333', label: 'People Dead' },
  { key: 'people_injured',     color: '#F5A623', label: 'People Injured' },
  { key: 'request_help',       color: '#FFD700', label: 'Need Rescue' },
  { key: 'safe_area',          color: '#1D9E75', label: 'Safe Area' },
  { key: 'safe_road',          color: '#378ADD', label: 'Safe Road' },
];

function getReportColor(report) {
  for (const { key, color } of REPORT_COLORS) {
    if (report[key]) return color;
  }
  return '#8B9AB0'; // fallback gray
}

function getReportLabel(report) {
  const labels = [];
  for (const { key, label } of REPORT_COLORS) {
    if (report[key]) labels.push(label);
  }
  return labels.length > 0 ? labels.join(', ') : 'Report';
}

function createMarkerIcon(color, confidence) {
  const opacity = 0.6 + (confidence * 0.4); // 0.6–1.0 based on confidence
  const size = confidence >= 0.8 ? 14 : 10;
  const glow = confidence >= 0.8 ? `0 0 10px ${color}` : `0 0 5px ${color}80`;

  return L.divIcon({
    className: '', // no default leaflet styles
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
    html: `<div style="
      width: ${size}px;
      height: ${size}px;
      border-radius: 50%;
      background: ${color};
      opacity: ${opacity};
      border: 2px solid rgba(255,255,255,0.8);
      box-shadow: ${glow};
      transition: all 0.3s ease;
    "></div>`,
  });
}

export default function ReportMarkers({ reports = [] }) {
  const map = useMap();
  const layerRef = useRef(null);

  useEffect(() => {
    if (layerRef.current) {
      layerRef.current.clearLayers();
    } else {
      layerRef.current = L.layerGroup().addTo(map);
    }

    if (!reports || reports.length === 0) return;

    reports.forEach(report => {
      const color = getReportColor(report);
      const label = getReportLabel(report);
      const confidence = report.confidence_score || 0.5;
      const icon = createMarkerIcon(color, confidence);

      const time = report.created_at
        ? new Date(report.created_at).toLocaleString([], {
            month: 'short', day: 'numeric',
            hour: '2-digit', minute: '2-digit',
          })
        : 'Unknown time';

      const confidencePct = Math.round(confidence * 100);
      const statusBadge = report.status === 'verified'
        ? '<span style="color:#1D9E75;font-weight:600;">✅ Verified</span>'
        : `<span style="color:#8B9AB0;">Confidence: ${confidencePct}%</span>`;

      const tooltipHtml = `
        <div style="font-size:12px;line-height:1.5;">
          <b style="color:#378ADD;">${label}</b><br/>
          ${statusBadge}<br/>
          <span style="color:#8B9AB0;">📍 ${report.latitude.toFixed(4)}, ${report.longitude.toFixed(4)}</span><br/>
          <span style="color:#8B9AB0;">🕐 ${time}</span>
          ${report.description ? `<br/><span style="color:#C0CCD8;">"${report.description.slice(0, 100)}${report.description.length > 100 ? '...' : ''}"</span>` : ''}
        </div>
      `;

      const marker = L.marker([report.latitude, report.longitude], { icon });
      marker.bindTooltip(tooltipHtml, {
        permanent: false,
        direction: 'top',
        offset: [0, -6],
      });

      layerRef.current.addLayer(marker);
    });
  }, [reports, map]);

  return null;
}
