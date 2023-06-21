import json
import datetime
from typing import Any

from conversion_tables import RouterNameTbm
from elastic_objects import ElasticDatabase

# def run_test():
#     metric_ids = []
#     def metrics(data: list[NetDeviceMetricObj]):
#         for i in range(2): print(data[i]); metric_ids.append(data[i].id)
#         return True

#     x = NetDeviceMetrics(time=(datetime.datetime.now()-datetime.timedelta(minutes=15)), 
#                          time_operation=Filter.greater_than, 
#                          fields=["id"])
#     try:
#         x.collect_pages(metrics)
#     except AssertionError as e:
#         print(e)

#     def devices(data: list[NetDevicesObj]):
#         for i in range(2): print(json.dumps(data[i].convert(), indent=2))
#         return True

#     # y = PageParser("net_devices", variables={"id__in": ",".join(metric_ids)})
#     y = NetDevices(variables={"id__in": ",".join(metric_ids)})
#     y.collect_pages(devices)

#     def routers(data: list[RoutersObj]):
#         for i in range(2): print(json.dumps(data[i].convert(), indent=2))
#         return True

#     z = Routers()
#     z.collect_pages(routers)

    # variables={"connection_state": "Connected"}
    # y = PageParser("net_devices")
    # y.collect_pages(local_testable)

import json as j
from cradlepoint import NetDeviceSignalSamples, NetDeviceSignalSamplesObj, HistoricalLocations, HistoricalLocationsObj, NetDeviceMetrics, NetDeviceMetricObj
from datetime import datetime, timedelta
import pytz

# def run_test():
#     interfaceable = RouterNameTbm()
#     table = interfaceable.collect(["46706930", "46706936", "74514431"])

#     print(j.dumps(table))


# def run_test():
#     elastic_client = ElasticDatabase()
#     # x = elastic_client.obliterate_index('cradlepoints')
#     # print(x)
#     with open('elastic_objects/cradlepoints.json') as f:
#         mappings: dict[Any, dict[str, dict]] = j.load(f)

#     x = elastic_client.create_index("cradlepoints", mappings.get("mappings")) # type: ignore
#     print(x)

def run_test():
    elastic_client = ElasticDatabase()
    # x = elastic_client.obliterate_index('cradlepoints')
    # print(x)
    x = elastic_client.es_client.indices.exists(index="cradlepoints")
    print(x)
    # with open('elastic_objects/cradlepoints.json') as f:
    #     mappings: dict[Any, dict[str, dict]] = j.load(f)

    # x = elastic_client.create_index("cradlepoints", mappings.get("mappings")) # type: ignore
    # print(x)

# def run_test():
#     x = NetDeviceSignalSamples(greater_than_time=( datetime.now(pytz.timezone("US/Mountain")) - timedelta(hours=1)), variables={"net_device__in": ",".join(["74574402", "80760226"])})
    
#     gatherable = []
#     def ur_mom(no: list[NetDeviceSignalSamplesObj]):
#         for i in no:
#             i = i.convert()
#             # print(i)
#             gatherable.append(i)
#     x.collect_pages(ur_mom)

#     counts = {}
#     for i in gatherable:
#         y = counts.get(i["net_id"], 0) + 1
#         counts[i["net_id"]] = y

#     print(counts)



# def run_test():
#     pass