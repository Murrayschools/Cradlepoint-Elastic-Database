from typing import Any, Callable
from datetime import datetime
from dacite import from_dict

from cradlepoint import TimeSortable
from .net_device_signal_samples_obj import NetDeviceSignalSamplesObj

class NetDeviceSignalSamples(TimeSortable):
    convert_to = NetDeviceSignalSamplesObj
    def __init__(self,
                 name: str = "page_parsed_data", 
                 less_than_time: datetime | None = None, 
                 greater_than_time: datetime | None = None,
                 variables: dict[str, str] = {}, 
                 fields: list[str] = []) -> None:
        url = "net_device_signal_samples/"
        super().__init__(url, "created_at", less_than_time, greater_than_time, name, variables, fields)


    def collect_pages(self, callback: Callable[[list[NetDeviceSignalSamplesObj]], bool | None]):
        return super().collect_pages(callback)