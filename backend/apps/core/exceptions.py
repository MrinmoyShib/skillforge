from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(response.data, dict):
            if 'detail' not in response.data:
                detail_msg = "; ".join([f"{k}: {', '.join(str(e) for e in v) if isinstance(v, list) else str(v)}" for k, v in response.data.items()])
            else:
                detail_val = response.data.get('detail', 'An error occurred.')
                detail_msg = "; ".join(str(e) for e in detail_val) if isinstance(detail_val, list) else str(detail_val)
        elif isinstance(response.data, list):
            detail_msg = "; ".join(str(e) for e in response.data)
        else:
            detail_msg = str(response.data) if response.data else 'An error occurred.'

        custom_response_data = {
            'detail': detail_msg,
            'code': getattr(exc, 'default_code', 'error'),
        }
        if isinstance(response.data, dict) and 'detail' not in response.data:
            custom_response_data['errors'] = response.data
        elif isinstance(response.data, list):
            custom_response_data['errors'] = response.data

        response.data = custom_response_data

    return response
