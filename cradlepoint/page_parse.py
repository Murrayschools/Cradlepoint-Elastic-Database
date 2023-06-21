from __future__ import annotations

from .cradlepoint_api import CradlepointAPI
from typing import Any, Callable
from dacite import from_dict
from .defaults import *
import json as j

class PageParser(CradlepointAPI):
    convert_to: type|None = None

    def __init__(self, 
                 endpoint: str, 
                 name: str = "page_parsed_data", 
                 variables: dict[str, str]={}, 
                 fields: list[str]=[]) -> None:
        # Fix endpoint
        super().__init__(495)
        endpoint = (endpoint if endpoint.endswith('/') else endpoint + "/")
        self.normal_url = starting_url+endpoint
        self.name = name
        self.data = []
        self.variables = variables
        if fields:
            self.variables.update({"fields": ",".join(fields)})


    @property
    def url(self):
        if not self.variables: return self.normal_url
        return f"{self.normal_url}?{ '&'.join( [f'{i}={self.variables.get(i)}' for i in self.variables.keys()] ) }"


    def build_pages(self):
        if len(self.data)!=0: self.data = []
        url = self.url

        while url:
            response = self.call(url)

            self.data.extend(response['data'])

            url = response['meta']['next']


    def collect_pages(self, callback: Callable[[list[Any]], bool|None]):
        '''
        Callback returns True to terminate
        '''
        url = self.url

        while url:
            data = self.call(url)

            # Generate next URL
            url = data['meta']['next']
            
            actual_data: list[dict] = data['data']

            # Calls the callback with it
            if callback(self._convert_pages(actual_data)): break


    def write_pages(self, folder: str = ""):
        with open(f'{folder}/{self.name}.json', 'w') as f:
            j.dump(self.data, f, indent=4)
    

    def _convert_pages(self, data: list[Any]):
        if self.convert_to == None: return data

        for count,i in enumerate(data):
            data[count] = from_dict(self.convert_to, i)

        return data