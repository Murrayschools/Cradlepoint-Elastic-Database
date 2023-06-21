from dotenv import load_dotenv
import os

load_dotenv()

default_headers = {
    'X-CP-API-ID': os.environ['X-CP-API-ID'],
    'X-CP-API-KEY': os.environ['X-CP-API-KEY'],

    'X-ECM-API-ID': os.environ['X-ECM-API-ID'],
    'X-ECM-API-KEY': os.environ['X-ECM-API-KEY'],

    'Content-Type': 'application/json' # This is required for all calls
}

starting_url = "https://www.cradlepointecm.com/api/v2/"