"""
Define functions/methods with are independent of business logic/requirement
"""
from rest_framework import status


# Get uniform formatted response with meta and data variables.
def get_formatted_response(data, st=status.HTTP_200_OK, success_bool=True):
    resp_dict = {
        "meta": {
            "success": success_bool,
            "status_code": st
        },
        "data": data
    }
    return resp_dict
