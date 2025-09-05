# Simon GO – Home Assistant (HACS)

Supported devices:
- **SWITCH / EW2W**
- **SWITCH D / EW1W**
- **DIMMER**
- **DIMMER W / ESW1W**
- **DIMMER RGBW / ESRGB1W / ESPIX1W**
- **SHUTTER / EZ1W / EZ1W.DC**
- **ROLLERGATE / EBR1W**
- **GATEBOX / EB1W, EB1W.PRO** and **DOORBOX / ED1W**
- **THERMOBOX / ET2W**
- **CONTROL / EK1W / EK4W** (buttons – exposed as `button` entities)


> Device states are **optimistic** (no status endpoints documented).  
> HA **services** are included for advanced options like `/forTime`, `toggle`, `inc/dec`, effects, presets, tilt, etc.

---

## Installation

### HACS (Custom repository)
1. In HACS → **Integrations** → ⋯ → **Custom repositories**.  
2. Add the repository URL (your fork or hosted repo).  
3. Category: **Integration**.  
4. Install **Simon GO** and **Restart Home Assistant**.

### Manual
1. Copy the folder `custom_components/simon_go` into your HA config directory.  
   Path: `config/custom_components/simon_go/`.  
2. Restart Home Assistant.  
3. Add integration: **Settings → Devices & services → + Add Integration → Simon GO**.

---

## Configuration

- Enter the **device IP** and **type**:  
  `switch`, `switch_d`, `dimmer`, `dimmer_w`, `dimmer_rgbw`,  
  `shutter`, `rollergate`, `gatebox`, `doorbox`, `thermo`, `control`.

- The integration will create appropriate entities:
  - `switch` → `switch` (1 channel)
  - `switch_d` → `switch` (2 channels)
  - `dimmer`, `dimmer_w` → `light` (brightness 0–255 → HEX `/s/00..FF`)
  - `dimmer_rgbw` → `light` (RGBW → `/s/RRGGBBWW`)
  - `shutter`, `rollergate`, `gatebox`, `doorbox` → `cover`
  - `thermo` → `climate`