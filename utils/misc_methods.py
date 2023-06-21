# import datetime
# from typing import Callable

# def wait_until(time_to: datetime.datetime, task: Callable[[], None]):

def get_endpoint_of_url(url: str):
    '''
    This function gets the end or
    endpoint of a url.

    EXAMPLE
    -

    >>> get_endpoint_of_url("https://www.cradlepointecm.com/api/v2/routers/2140151/")
    "2140151"
    '''
    if not url.endswith("/"):
        url += "/"
    new_url = url.removesuffix("/")
    index = new_url.rfind("/")
    return url[index+1:-1]