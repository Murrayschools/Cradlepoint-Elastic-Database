from typing import Callable, Any
from dacite import from_dict

from cradlepoint import PageParser
from .routers_obj import RoutersObj

class Routers(PageParser):
    def __init__(self,
                 name: str = "routers",
                 variables: dict[str, str] = {},
                 fields: list[str] = []) -> None:
        url = "routers/"
        super().__init__(url, name, variables, fields)

    def collect_pages(self, callback: Callable[[list[RoutersObj]], bool | None]):
        def local_callback(data: Any):
            for count,i in enumerate(data):
                # Because netcloud made id a string, even though the docs
                # says it is an int -_-
                i['id'] = int(i['id'])
                # Converts each router data to a data type
                data[count] = from_dict(RoutersObj, i)
            return callback(data)
        
        super().collect_pages(local_callback)