from typing import Any, Callable
from dacite import from_dict

from cradlepoint import PageParser, Filter
from .net_devices_obj import NetDevicesObj

class NetDevices(PageParser):
    def __init__(self, 
                 name: str = "page_parsed_data", 
                 variables: dict[str, str] = {}, 
                 fields: list[str] = []) -> None:
        url = "net_devices/"
        super().__init__(url, name, variables, fields)

    def collect_pages(self, callback: Callable[[list[NetDevicesObj]], bool | None]):
        def local_callback(data: Any):
            for count,i in enumerate(data):
                # Because netcloud made id a string, even though the docs
                # says it is an int -_-
                # i['id'] = int(i['id'])
                # Although that is the case, I'm going to stick with 
                # str just in case
                # Converts each router data to a data type
                data[count] = from_dict(NetDevicesObj, i)
            return callback(data)
                
        super().collect_pages(local_callback)