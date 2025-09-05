DOMAIN = "simon_go"

CONF_HOST = "host"
CONF_DEVICE_TYPE = "device_type"
CONF_NAME = "name"

DEVICE_TYPES = [
    "switch",
    "switch_d",
    "dimmer",
    "dimmer_w",
    "dimmer_rgbw",
    "shutter",
    "rollergate",
    "gatebox",
    "doorbox",
    "thermo",
    "control",
]

PLATFORM_MAP = {
    "switch": ["switch"],
    "switch_d": ["switch"],
    "dimmer": ["light"],
    "dimmer_w": ["light"],
    "dimmer_rgbw": ["light"],
    "shutter": ["cover"],
    "rollergate": ["cover"],
    "gatebox": ["cover"],
    "doorbox": ["cover"],
    "thermo": ["climate"],
    "control": ["button"],
}
