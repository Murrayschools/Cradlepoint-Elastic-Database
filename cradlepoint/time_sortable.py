from datetime import datetime

from .page_parse import PageParser
from .filter import Filter

class TimeSortable(PageParser):
    def __init__(self, 
                 endpoint: str, 
                 time_var_name: str,
                 less_than_time: datetime | None = None, 
                 greater_than_time: datetime | None = None,
                 name: str = "page_parsed_data", 
                 variables: dict[str, str] = {}, 
                 fields: list[str] = []) -> None:
        super().__init__(endpoint, name, self.assemble_vars(time_var_name, less_than_time, greater_than_time, variables), fields)


    def assemble_vars(self, 
                      time_var_name: str,
                      less_than_time: datetime | None, 
                      greater_than_time: datetime | None, 
                      variables: dict) -> dict:
        new_variables: dict = variables
        if less_than_time:    new_variables.update({(time_var_name+Filter.less_than.value): less_than_time.isoformat().replace("+", "%2b")})
        if greater_than_time: new_variables.update({(time_var_name+Filter.greater_than.value): greater_than_time.isoformat().replace("+", "%2b")})
        
        return new_variables