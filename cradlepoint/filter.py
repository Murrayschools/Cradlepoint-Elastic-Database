from enum import Enum

class Filter(Enum):
    includes = "__in"    # includes
    greater_than = "__gt"    # greater than
    greater_equal= "__gte"   # greater than or equal to
    less_than = "__lt"    # less than
    less_equal= "__lte"   # less than or equal to