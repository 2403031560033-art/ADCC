# ADCC — UI Layout Specification
# DO NOT REARRANGE SECTIONS

---

## Global Layout

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER — Logo "ADCC" | Status badge | Scenario name        │
│           "Operation Brahmaputra" | [Trigger Disaster] btn   │
├──────────┬──────────┬──────────┬──────────────────────────── │
│  KPI     │  KPI     │  KPI     │  KPI                        │
│  42%     │  67%     │  91%     │  3,200                      │
│ Response │Efficiency│ Supplies │  Lives                      │
├──────────┴──────────┴──────────┴─────────────────────────────┤
│                                                              │
│                   LEAFLET MAP                                │
│     (zones as circles, hospitals as pins, routes as lines)  │
│                                                              │
├──────────────────────────┬───────────────────────────────────┤
│  TIMELINE                │  AGENT ACTIVITY PANEL             │
│  (chronological events)  │  (5 agent cards, live reasoning)  │
└──────────────────────────┴───────────────────────────────────┘
```

---

## Component Specs

### HEADER
- Left: "ADCC" wordmark in monospace, red dot for live status
- Center: Scenario badge ("🌊 Operation Brahmaputra · Assam · Flood")
- Right: "[▶ Trigger Disaster]" button — primary CTA, orange (#E8410A)

### KPI CARDS (4 cards, horizontal row)
- Background: dark card on dark surface
- Value: large number (32px+), colored green when active
- Label: small, muted text below value
- Cards animate from 0 → target on disaster trigger

### MAP
- Full width, min-height 400px
- Zone circles: red = severity 8-10, orange = 5-7, yellow = 1-4
- Hospitals: blue pin icon
- Warehouses: orange warehouse icon
- Blocked roads: dashed red line
- Active routes: solid green polyline with animated direction
- Drone paths: dashed blue line

### TIMELINE (left column, bottom)
- Vertical list, newest at top
- Each entry: timestamp | agent name | action
- Color-coded by agent (match Agent Roster colors from SOURCE_OF_TRUTH.md)
- Auto-scrolls to latest event

### AGENT ACTIVITY PANEL (right column, bottom)
- 5 rows, one per agent
- Each row: colored dot | agent name | last action text
- "Thinking..." state when agent is processing
- "Done" badge when agent completes task
- Pulse animation on active agent

---

## Color Tokens

```
Background (dark):   #0A1628
Surface card:        #0F1E35
Border:              #1E3050
Emergency orange:    #E8410A
Safe green:          #1D9E75
Steel blue:          #378ADD
Text primary:        #F4F5F7
Text muted:          #8B9AB0
```

---

## Responsive Rules

- Below 768px: Map goes full width, Timeline and Agent Panel stack vertically
- KPI cards wrap to 2×2 grid on mobile
- Header collapses to icon + title only on mobile
