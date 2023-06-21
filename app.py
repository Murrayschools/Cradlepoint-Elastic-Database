'''
SOFTWARE WRITTEN BY LOGAN CEDERLOF
DATE (as of writing): May 2nd, 2023
ESTIMATED START DATE: April 14th, 2023

The goal of this program is to act as a
middle software between Cradlepoint and
the Elastic Stack. Data is taken from
the V2 Cradlepoint API, and delivered
to the "cradlepoints" index inside
ElasticSearch 8.x.

Cradlepoint is talked to using their
RestAPI, and a library that I have
created and expanded called 
"cradlepoint".

ElasticSearch is talked to using
their python client wrapped in
an object that I have made.

This file serves as the base, and 
interacts with the other objects 
and libraries; the real magic 
happens inside of those libraries
I have created.
'''

# EVIRONMENT INITIATION
from dotenv import load_dotenv
load_dotenv()

# LIBRARY IMPORTS
# My libraries
from elastic_objects import ElasticDatabase
from cradlepoint import NetDeviceMetrics, NetDeviceMetricObj, NetDeviceSignalSamples, NetDeviceSignalSamplesObj
from conversion_tables import RouterNameTbm
from resources import ResourceManager
from resources.state import SessionData
from utils import start_logging
from tests import run_test

# Other libraries
from typing import Any
import traceback
import json as j
import datetime
import pytz
import sys
import os

if os.environ["TEST-MODE"].upper() == "TRUE":
    run_test()
    sys.exit(0)

# Setup logging
logger = start_logging()

# Setup globals
elastic_client = ElasticDatabase()
update_interval: int = int(os.environ["UPDATE-INTERVAL"])


def get_time_ago(current_time: datetime.datetime) -> datetime.datetime:
    last_time: SessionData = ResourceManager.session_data.value
    time_retrieved = datetime.datetime.fromisoformat(last_time.time_of_collection)
    max_limit_ago = current_time - datetime.timedelta(hours=5)
    if (time_retrieved) < (max_limit_ago):
        return max_limit_ago
    else:
        return time_retrieved


def add_table_data(table: dict, data: dict, id_name: str = "net_id") -> dict:
    extendable = table.get(data[id_name]) # After conversion, id becomes net_id
    if (extendable != None): 
        data.update(extendable)
    else: logger.error("router_id, asset_id, and custom1 not found.")
    return data


def get_signal_samples(last_time: datetime.datetime, net_ids: list):
    ndss = NetDeviceSignalSamples(greater_than_time=last_time, variables={"limit": "100", "net_device__in": ",".join(net_ids)})
    returnable: list = []
    def signal_sample_page(part: list[NetDeviceSignalSamplesObj]):
        for i in part:
            returnable.append( i.convert() )
    ndss.collect_pages(signal_sample_page)
    return returnable


def add_data_to_elastic(data: list[dict]):
    for i in data:
        elastic_client.index_data(index_name="cradlepoints", data=i)


def router_metrics(last_time: datetime.datetime, hard_table: RouterNameTbm):
    ndm = NetDeviceMetrics(greater_than_time=last_time, fields=["id", "cell_id", "service_type"], variables={"limit": "100"})
    def net_device_page(part: list[NetDeviceMetricObj]):
        data = {}
        # For each item in router metrics page
        for i in part:
            # Create a hashmap on data
            data[i.id] = {"cell_id": i.cell_id, "service_type": i.service_type}

        # Get all relevant net_ids
        net_ids = list( data.keys() )

        # Get hasmap from the router tables using the ids
        router_table = hard_table.collect(net_ids) # type: ignore
        # Update the data with the router data
        for k,v in router_table.items():
            data[k].update(v)

        # Get the signal samples
        signal_samples = get_signal_samples(last_time, net_ids)

        for i in signal_samples:
            appendable = data.get(i["net_id"], None)
            i.update(appendable)
        
        add_data_to_elastic(signal_samples)

    ndm.collect_pages(net_device_page)


def verify_cradlepoints_index() -> bool:
    '''
    Returns true if a new index
    was created.
    '''
    if elastic_client.index_exists("cradlepoints"): return False

    with open('elastic_objects/cradlepoints.json') as f:
        mappings: dict[Any, dict[str, dict]] = j.load(f)
    x = elastic_client.create_index("cradlepoints", mappings.get("mappings")) # type: ignore
    logger.info(f"Create index attempted. Response: {x}")
    return True


# Begin database client
def main(current_time: datetime.datetime):
    last_time = get_time_ago(current_time)
    verify_cradlepoints_index()
    logger.info(f"The previous fetch began at {last_time}")

    table = RouterNameTbm()

    router_metrics(last_time, table)


if __name__ == "__main__":
    current_time = datetime.datetime.now(pytz.timezone('US/Mountain'))
    try:
        main(current_time)
    except Exception:
        logger.critical(traceback.format_exc())
    ResourceManager.session_data.value.time_of_collection = current_time.isoformat()
    ResourceManager.write()
        