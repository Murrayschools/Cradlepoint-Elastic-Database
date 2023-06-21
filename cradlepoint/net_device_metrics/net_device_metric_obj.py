from dataclasses import dataclass, asdict

@dataclass
class NetDeviceMetricObj:
    update_ts: str | None
    # This is a string because
    # the API stores it as a 
    # string
    id: str | None

    rssi: int | None
    rsrp: float | None
    rsrq: float | None
    sinr: float | None
    signal_strength: int | None
    dbm: int | None
    service_type: str | None
    cell_id: str | None

    def convert(self) -> dict:
        x = asdict(self)
        if "update_ts" in x.keys():
            x["@timestamp"] = x.pop("update_ts")
            x["net_id"] = x.pop("id")
        return x
