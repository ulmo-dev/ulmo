class NoDataError(Exception):
    """Error to be raised when pyhis can't extract data from a waterml
    response (either because the response contains no data or the
    response is invalid)
    """
    pass
