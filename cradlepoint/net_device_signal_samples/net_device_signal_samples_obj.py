from dataclasses import dataclass, asdict
from typing import Any
from utils import get_endpoint_of_url

@dataclass
class NetDeviceSignalSamplesObj():
    created_at: str | None

    rsrp: float | None
    rsrp5g: float | None
    rsrp5g_highband: float | None

    rsrq: float | None
    rsrq5g: float | None
    rsrq5g_highband: float | None

    sinr: float | None
    sinr5g: float | None
    sinr5g_highband: float | None

    # These values can be "Any" because
    # cradlepoint has a tendency to 
    # return values of strings instead
    # of numbers (even though it says 
    # it will return numbers in the docs). 
    # So until we know
    # exactly what it is, all I can
    # put is "Any" for safety reasons.
    dbm: int | None
    ecio: Any | None

    rssi: Any | None
    rssnr: Any | None

    signal_percent: int | None
    net_device: str | None


    def convert(self):
        x = asdict(self)
        x["@timestamp"] = x.pop("created_at")
        x["net_id"] = get_endpoint_of_url(x.pop("net_device"))
        return x