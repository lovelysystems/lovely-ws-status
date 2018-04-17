from pyramid.view import view_config

# If the prometheus client is available we will provide the prometheus metrics
try:
    from prometheus_client import generate_latest
except:
    # provide a dummy if the prometheus_client package is not available
    def generate_latest():
        return b''


from . import STATUS_HANDLERS, NUMERIC_VALUES


@view_config(route_name='svc_status')
def svc_status_view(request):
    """Provides more detailed information about the status of the service.

    The status is provided by status handlers which are registered in the
    status module.
    """
    response = request.response
    result = {}
    for name, handler in STATUS_HANDLERS.items():
        result[name] = handler()
    accept = request.headers.get('accept')
    as_csv = accept and 'text/csv' in accept
    as_json = accept and 'application/json' in accept
    t = request.matchdict.get('type', '')
    if not as_csv and not as_json:
        as_json = t == '.json'
    if t == '.prometheus':
        response.content_type = 'text/plain; version=0.0.4'
        lines = []
        for name, status in sorted(result.items()):
            lines.append('# HELP svc_status Status 0->OK, 1->YELLOW, 2->RED')
            lines.append('# TYPE svc_status untyped')
            lines.append('svc_status{{name="{name}"}} {value}'.format(
                name=name,
                value=NUMERIC_VALUES.get(status.get('state'), 0)
            ))
            # additional optional labels
            labels = status.get('labels')
            if isinstance(labels, dict):
                for label, value in labels.items():
                    lines.append(
                        'svc_status{{name="{prefix}_{name}"}} {value}'.format(
                            prefix=name,
                            name=label,
                            value=value
                        )
                    )
        lines.append('')  # new line required after every metric
        result = u'\n'.join(lines)
        result += generate_latest().decode('utf-8')
        response.text = result
    elif as_json:
        response.content_type = 'application/json'
        response.json = result
    else:
        response.content_type = 'text/csv'
        lines = []
        for name, status in sorted(result.items()):
            lines.append('{name}\t{state}\t{detail}'.format(
                                name=name,
                                state=status.get('state', ''),
                                detail=status.get('detail', '')
                                ))
        response.text = u'\n'.join(lines)
    return response


def includeme(config):
    config.add_route("svc_status",
                     "/svc_status{type:(|.json|.csv|.prometheus)}")
