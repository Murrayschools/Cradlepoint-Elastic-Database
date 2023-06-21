from datetime import datetime
from typing import Any, Callable
from dacite import from_dict

from cradlepoint import TimeSortable, Filter
from .net_device_metric_obj import NetDeviceMetricObj

class NetDeviceMetrics(TimeSortable):
    def __init__(self, 
                 name: str = "device_metrics", 
                 less_than_time: datetime | None = None, 
                 greater_than_time: datetime | None = None,
                 variables: dict[str, str] = {},
                 fields: list[str] = []) -> None:
        url = "net_device_metrics/"
        # super().__init__(url, name, self.assemble_vars(less_than_time, greater_than_time, variables), fields)
        super().__init__(url, "update_ts", less_than_time, greater_than_time, name, variables, fields)


    def collect_pages(self, callback: Callable[[list[NetDeviceMetricObj]], bool | None]):
        def local_callback(data: Any):
            for count,i in enumerate(data):
                # Converts each router data to a data type
                data[count] = from_dict(NetDeviceMetricObj, i)
            return callback(data)
                
        super().collect_pages(local_callback)
