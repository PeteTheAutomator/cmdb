RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

schema = {
    'instance_id': {
        'type': 'string',
        'minlength': 10,
        'maxlength': 10,
        'required': True,
    },
    'rpm_packages': {
        'type': 'list',
        'required': False,
    },
}

audits = {
    'item_title': 'audit',
    'additional_lookup': {
        'url': 'regex("[\w\d\-]+")',
        'field': 'instance_id'
    },
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,
    'resource_methods': ['GET', 'POST'],
    'schema': schema
}

DOMAIN = {
    'audits': audits,
}