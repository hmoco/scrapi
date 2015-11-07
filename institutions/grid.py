import json
import logging
from schema_transformer.transformer import JSONTransformer

from .institutions import Institution

logger = logging.getLogger(__name__)

class GridTransformer(JSONTransformer):
    pass

schema = {
    'name': ('/name', lambda x: x.encode('utf8') if x else None),
    'location': {
        'street_address': ('/addresses', lambda x: x[0]['line_1'] if x else None),
        'city': ('/addresses', lambda x: x[0]['city'] if x else None),
        'state': ('/addresses', lambda x: x[0]['state'] if x else None),
        'ext_code': ('/addresses', lambda x: x[0]['postcode'] if x else None),
        'country': ('/addresses', lambda x: x[0]['country'] if x else None)
    },
    'web_url': ('/links', lambda x: x[0] if x else None),
    'id_': '/id',
    'other_names': ('/aliases', '/acronyms', lambda x, y: x + y if x and y else x if x else y if y else None)
}

def get_jsons(grid_file):
    with open(grid_file) as f:
        f.readline() # Pop off the top
        f.readline()
        for line in f:
            try:
                yield json.loads(line[:-2])
            except ValueError:
                yield json.loads(line)
                break

def populate(grid_file):
    transformer = GridTransformer(schema)
    for doc in get_jsons(grid_file):
        transformed = transformer.transform(doc, load=False)
        try:
            inst = Institution(**transformed)
            inst.save()
        except UnicodeDecodeError:
            print (transformed)