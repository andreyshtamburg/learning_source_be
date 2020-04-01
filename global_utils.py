def get_global_parser(ns):
    """
    add x-client header param for swagger
    :param ns: namespace
    :return: parser
    """
    parser = ns.parser()
    parser.add_argument('x-client', type=str, location='headers', required=True)
    return parser


# x-client header param excluded url patterns
# accept_url_patterns = [
#     r'/api/v1/doc/',
#     r'/api/v1/swagger.json',
#     r'/swaggerui/*'
# ]


# accept URL endpoints
accept_endpoints = [
    'restplus_doc.static',
    'v1_blueprint.doc',
    'v1_blueprint.specs'
]
