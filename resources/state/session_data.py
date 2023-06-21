from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class SessionData:
    time_of_collection: str # iso format
    router_clean_up_ago: str # iso format