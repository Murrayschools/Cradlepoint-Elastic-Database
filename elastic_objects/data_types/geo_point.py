from dataclasses import dataclass, asdict

@dataclass
class GeoPoint:
    latitude: float | None
    longitude: float | None

    # def convert()
    convert = lambda self: asdict(self)
    __call__ = lambda self: self.convert()