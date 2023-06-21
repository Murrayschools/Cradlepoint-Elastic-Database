from datetime import datetime
from dacite import from_dict

from .historical_locations_obj import HistoricalLocationsObj
from cradlepoint import TimeSortable

class HistoricalLocations(TimeSortable):
    convert_to = HistoricalLocationsObj
    def __init__(self, 
                 less_than_time: datetime | None = None, 
                 greater_than_time: datetime | None = None, 
                 name: str = "Historical Locations Data", 
                 variables: dict[str, str] = {}, 
                 fields: list[str] = []) -> None:
        url = "historical_locations/"
        super().__init__(url, "created_at", less_than_time, greater_than_time, name, variables, fields)

