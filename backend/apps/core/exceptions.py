from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(response.data, dict) and 'detail' not in response.data:
            detail_msg = "; ".join([f"{k}: {', '.join(str(e) for e in v) if isinstance(v, list) else str(v)}" for k, v in response.data.items()])
        else:
            detail_msg = response.data.get('detail', 'An error occurred.') if isinstance(response.data, dict) else response.data

        custom_response_data = {
            'detail': detail_msg,
            'code': getattr(exc, 'default_code', 'error'),
        }
        if isinstance(response.data, dict) and 'detail' not in response.data:
            custom_response_data['errors'] = response.data

        response.data = custom_response_data

    return response
