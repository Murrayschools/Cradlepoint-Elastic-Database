from cradlepoint import NetDeviceMetrics, NetDeviceMetricObj

class TowerIdTable:
    def __init__(self):
        self.items: dict[str, str] = {}

    def __discover_items(self, net_devices: list[str], last_time) -> dict[str, str]:
        '''
        returns
        "net_device": "cell_id"
        '''
        returnable: dict[str, str] = {}
        def fetch(x: list[NetDeviceMetricObj]):
            for i in x:
                if i.id == None: continue
                returnable[i.id] = i.cell_id or ""

        NetDeviceMetrics(greater_than_time=last_time, fields=["cell_id", "id"], variables={"id__in": ",".join(net_devices)}).collect_pages(fetch)
        return returnable
    
    def get_items(self, net_devices: list[str], last_time) -> dict[str, str]:
        returnable = {}
        need_to_discover: list[str] = []

        for i in net_devices:
            if x:=self.items.get(i, None):
                returnable.update({i: x})
            else:
                need_to_discover.append(i)

        discovered = self.__discover_items(need_to_discover, last_time)
        self.items.update(discovered)
        returnable.update(discovered)
        return returnable