from cradlepoint import NetDeviceMetrics, Filter
import datetime

def test_net_device_metric_timestamp():
    x = NetDeviceMetrics(time=datetime.datetime.fromisoformat("2023-04-24T20:12:56.416578+00:00"), time_operation=Filter.greater_than)
    assert x.url == "https://www.cradlepointecm.com/api/v2/net_device_metrics/?update_ts__gt=2023-04-24T20:12:56.416578%2b00:00"