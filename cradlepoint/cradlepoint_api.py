import time
from typing import TypedDict
from .defaults import *
from utils import get_current_logger
import requests as r
import datetime

logger = get_current_logger()

class Meta(TypedDict):
    limit: int
    next: str | None
    previous: str | None

class GenericResponse(TypedDict):
    data: list
    meta: Meta

class CradlepointAPI:
    last_call_time: datetime.datetime | None = None


    def __init__(self, limit_a_min: int):
        self.limit_between = (60 / limit_a_min) # Get 


    def __get_time_delta(self):
        '''
        Get the amount of time passed
        between now and last call time
        '''
        if CradlepointAPI.last_call_time == None: 
            raise TypeError("Last call time cannot be none")
        return datetime.datetime.now() - CradlepointAPI.last_call_time


    def __bottle_neck(self):
        '''
        This caps the amount of 
        time in between each call
        '''
        if CradlepointAPI.last_call_time == None: return
        
        while self.__get_time_delta() < datetime.timedelta(seconds=self.limit_between):
            pass

    
    def _get_exception_data(self, data):
        # Because the unauthorized type of exception has a str for its exception
        # key, we must check if the exception is a str or if it is a dict
        return data.get('exception') if isinstance(data.get('exception'), str) else data.get('exception').get('message')
    

    def call(self, url: str, extra_headers: dict | None = None) -> GenericResponse:
        '''
        Returns the raw data from the
        CradlePoint API. Returns an
        AssertionError if the API
        gives a bad response.

        Example
        =
        ```
        {
            "data": 
                [ data ]
            "meta": {
                "next": url | None
                "previous": url | None
                "limit": int
            }
        }
        ```
        '''
        headers = default_headers.copy()
        if extra_headers:
            headers.update(extra_headers)

        start_time = time.perf_counter()
        self.__bottle_neck()
        bottleneck_text = f"The bottleneck took {time.perf_counter()-start_time}s"
        logger.info(bottleneck_text)
        print(bottleneck_text)
        response = r.get(url, headers=headers)
        CradlepointAPI.last_call_time = datetime.datetime.now()

        # Convert to json
        data: dict = response.json()   
    
        assert not data.get("exception", False), f"A code of {response.status_code} was given, and there were some errors when making the request: {self._get_exception_data(data)}"

        return data # type: ignore
    