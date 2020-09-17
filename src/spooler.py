# mockable spool decorator
# in python shell / tests, uwsgi module is not available
# so we need to wrap the import in a try/except block
try:
    from uwsgidecorators import spool
except ModuleNotFoundError:
    spool = None # leaves it to mock

"""
Function that converts arguments to byte arrays as required by uWSGI spooler.
"""
def prepare_spooler_args(**kwargs):
    args = {}
    for name, value in kwargs.items():
        args[name.encode('utf-8')] = str(value).encode('utf-8')
    return args
