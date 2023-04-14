#generic response are written to return error message to frontend

def success_response(data, message, error_message, state):
    response = {
        "result": data,
        "message": message,
        "error_message": error_message,
        "status_code": state,
        "status": True
    }
    return response

def failed_response(data, message, error_message, state):
    response = {
        "result": data,
        "message": message,
        "error_message": error_message,
        "status_code": state,
        "status": True
    }
    return response

def error_response(data, message, error_message, state):
    response = {
        "result": data,
        "message": message,
        "error_message": error_message,
        "status_code": state,
        "status": False
    }
    return response
