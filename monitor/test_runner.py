import time, requests
from .models import TestRun

def execute_request(endpoint, url, method):
    start_time = time.perf_counter()
    status_code = None
    success = False
    error_msg = ""
    
    try:
        response = requests.request(
                method=method,
                url=url,
                timeout=10
            )
        status_code = response.status_code
        success = 200 <= status_code <= 299
    except requests.exceptions.RequestException as error:
        error_msg = str(error)
    
    elapsed_time = round((time.perf_counter()-start_time)*1000, 2)
    
    TestRun.objects.create(
        endpoint=endpoint,
        status_code=status_code,
        success=success,
        response_time_ms=elapsed_time,
        error_msg=error_msg
    )
    
    return{
        "status_code" : status_code,
        "request_time_ms" : elapsed_time,
        "success" : success,
        "error_msg" : error_msg
    }