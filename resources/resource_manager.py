from datetime import datetime, timedelta
from dataclasses import asdict
from typing import Any, overload
import json as j
import os

from .state import SessionData

resources_folder = "resources/"

class StateResource:
    state_location = f"{resources_folder}state/"
    @overload
    def __init__(self, name: str, default: str, data_type: type) -> None: 
        '''
        A resource that is considered a state (preserved
        between the times when the program is ran), and 
        requires a default value in case their is no
        saved state. 

        For the default state, give the name of a file 
        located in the state folder.
        '''
        ...
    @overload
    def __init__(self, name: str, default: Any, data_type: type) -> None: 
        '''
        A resource that is considered a state (preserved
        between the times when the program is ran), and 
        requires a default value in case their is no
        saved state. 

        For the default state, give an object of data
        type `data_type`
        '''
        ...

    def __init__(self, name, default, data_type) -> None:
        self.path = self.state_location+name
        self.data_type = data_type

        if type(default) == str:
            with open(self.state_location+default) as f:
                self.default = data_type(**j.load(f))
        else:
            self.default = default
            
        self.read()


    @property
    def value(self):
        if not self._value:
            self.read()
        return self._value;


    @value.setter
    def value(self, value):
        self._value = value
        return value


    def get(self):
        return self.value


    def read(self) -> Any:
        if not os.path.isfile(self.path): 
            self.value = self.default
            return self.default

        with open(self.path) as f:
            x = j.load(f)
        self.value = self.data_type(**x)
        return self.value


    def write(self) -> None:
        writable = asdict(self.value)
        with open(self.path, 'w') as f:
            j.dump(writable, f)



class ResourceManager:
    session_data = StateResource(
        "session_data.json", 
        "session_data_default.json", # Default is a time of 5 minutes ago
        SessionData
    )

    states = [session_data]

    @classmethod
    def write(cls):
        for i in cls.states:
            i.write()