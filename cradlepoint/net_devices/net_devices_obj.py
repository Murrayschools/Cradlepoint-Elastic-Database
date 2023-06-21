from dataclasses import dataclass, asdict


# NOTE: Not all types are here; only needed ones are.
# However, in the event you need a specific one,
# simply add it here, as well as its data type
# and a None type. That field will automatically
# then be populated.
@dataclass
class NetDevicesObj:
    id: str | None
    serial: str | None
    account: str | None
    apn: str | None
    bsid: str | None
    imei: str | None
    is_asset: bool | None
    router: str | None

    def convert(self) -> dict:
        x = asdict(self)

        # Conversion operations

        return x
    