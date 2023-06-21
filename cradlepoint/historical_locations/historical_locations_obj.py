from dataclasses import dataclass

@dataclass
class HistoricalLocationsObj:
    accuracy: float | None
    created_at: str | None
    dbm: int | None
    signal_percent: int | None

    rfband: str | None
    rfband_5g: str | None
    rsrp: float | None
    rsrp_5g: float | None
    rsrq: int | None
    rsrq_5g: int | None
    sinr: int | None
    sinr_5g: int | None

    latitude: int | None
    longitude: int | None