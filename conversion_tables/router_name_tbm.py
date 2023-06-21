from cradlepoint import NetDevices, NetDevicesObj, Routers, RoutersObj
from datetime import datetime, timedelta
from resources import ResourceManager
from utils import get_endpoint_of_url
import logging
import pytz
import csv
import os

routers_file_name: str = "conversion_tables/tbs/routers.csv"
logger = logging.getLogger(os.environ["LOGGER-NAME"])

fieldnames = ["net_device", "router_id", "asset_id", "custom1"]

class RouterNameTbm():
    '''
    Interface object for router tables
    '''
    def __init__(self):
        self._extras: dict[str, dict[str, str]] = {}
        self.read_table()


    def write_changes(self):
        '''
        Writes to the local table
        '''
        self.data: dict
        with open(routers_file_name, mode='w') as router_data:
            writeable = csv.DictWriter(router_data, fieldnames=fieldnames)

            writeable.writeheader()
            for net_device, remaining in self.data.items():
                # This converts the net_device: attributes into a list of lists
                row: dict = remaining.copy() 
                row.update({"net_device": net_device})
                writeable.writerow(row)


    def table_cleanup(self) -> bool:
        '''
        This function removes the 
        router table every 12 hours
        to ensure that the database
        is using the "latest" data.

        Returns true if the router 
        table was deleted, or if it
        didn't exist in the first 
        place
        '''
        if not os.path.isfile(routers_file_name): return True

        session_data = ResourceManager.session_data.value
        then = datetime.fromisoformat(session_data.router_clean_up_ago)
        now = datetime.now(pytz.utc)

        # If it has not been 12 hours since last table removal
        if not ((now.hour == 12 or now.minute == 0) or (now-then > timedelta(hours=12))):
            return False

        os.remove(routers_file_name)
        session_data.router_clean_up_ago = now.isoformat()
        return True
    

    def read_table(self):
        '''
        Reads the local table, and 
        adds it into the object's
        `data` attribute.
        '''
        self.data: dict = {}
        if self.table_cleanup(): return 

        with open(routers_file_name, mode='r') as router_data:
            reader = csv.DictReader(router_data)
            mapped_data: list = [element for element in reader]
            # This converts the list of list into a net_device: attributes
            for i in mapped_data:
                row = i.copy()
                row.pop("net_device")
                self.data[i["net_device"]] = row


    def __get_router_ids(self, net_devices: dict) -> dict:
        '''
        Gets router ids based off of the following table:

        ```
        "net_id": {}
        ```

        and converts it to:

        ```
        "net_id": {
            "router_id": str
        }
        ```
        '''
        def net_device_get(data: list[NetDevicesObj]):
            print(f"This is what the server sent for new routers: {data}")
            for i in data: 
                i: NetDevicesObj
                if i.router == None: logger.error('Router id cannot be found.'); break

                # router_ids.append(int(get_endpoint_of_url(i.router)))
                net_devices[i.id].update( {"router_id": get_endpoint_of_url(i.router)} )

        NetDevices(fields=["router", "id"], variables={"id__in": ",".join([str(i) for i in net_devices.keys()])}).collect_pages(net_device_get)
        return net_devices


    def __get_router_info(self, table: dict) -> dict:
        '''
        Delivers Asset IDs, and Custom1s respectively

        This is done by being given the partial table:

        ```
        "net_device": {
            "router_id": str
        }
        ```
        Which is then converted into:
        ```
        "net_device": {
            "router_id": str
            "asset_id": str
            "custom1": str
        }
        ```
        '''

        def routers_get(data: list[RoutersObj]):
            for key, value in table.items():
                data_index: int|None = None # findable is the index of the data
                for index,router in enumerate(data):
                    i: RoutersObj
                    if router.id == None: logger.error("Somehow the id of the router is null."); continue
                    if str(router.id) == value.get("router_id"): data_index = index; break

                if data_index == None:
                    table[key].update({"asset_id": ""}) 
                    table[key].update({"custom1": ""}) 
                    continue

                asset_id = data[data_index].asset_id if data[data_index].asset_id != None else ""
                custom1 = data[data_index].custom1 if data[data_index].custom1 != None else ""

                table[key].update({"asset_id": asset_id}) 
                table[key].update({"custom1": custom1}) 

        print(table)
        Routers(fields=["id", "asset_id", "custom1"], variables={"id__in": ",".join( [i["router_id"] for i in table.values() if i.get("router_id", False)] )}).collect_pages(routers_get)
        return table
    

    def __search_local(self, net_devices: list[str]) -> tuple[dict, list[str]]:
        '''
        EXPLANATION
        -
        This method searches the local router tables 
        for conversions. 

        RETURNS
        -
        In a tuple, it returns the table, as well as 
        the list of devices to collect from the server.

        The table is a dictionary, with the net_device 
        as the key, and the rest as values.
        '''
        if not os.path.isfile(routers_file_name): return ({}, net_devices)

        need_to_gather: list[str] = []
        table: dict = {}
        for i in net_devices:
            device = self.data.get(i, None)

            if device == None: need_to_gather.append(i); continue
            table[i] = device

        return (table, need_to_gather)
    

    @property
    def full_table(self):
        '''
        Gives the saved table
        plus the temporary one.
        '''
        if not self._extras: return self.data

        x = self.data.copy()
        for key, value in self._extras.items():
            x[key].update(value)
        return x


    def collect(self, net_devices: list[str]):
        '''
        Returns a table using the NET IDS given:

        ```
        "net_device": {
            "router_id": str
            "asset_id": str
            "custom1": str
        }
        ```

        This is done either by looking through
        local tables, and/or searching the API
        '''
        table, nd_left= self.__search_local(net_devices)

        if nd_left == []: return table

        table_left: dict = {}
        for i in nd_left:
            table_left[i] = {}

        router_ids = self.__get_router_ids(table_left)
        remaining_table = self.__get_router_info(router_ids)

        self.data.update(remaining_table)

        self.write_changes()

        table.update(remaining_table)

        return table
    