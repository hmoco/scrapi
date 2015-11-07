from elasticsearch_dsl import DocType, String, Date, Boolean, Integer
from elasticsearch_dsl.connections import connections

from scrapi.settings import ELASTIC_URI, ELASTIC_INST_INDEX

connections.create_connection(hosts=[ELASTIC_URI])

def main():
    Institution.init()

class Institution(DocType):
    name = String()
    established = String()
    location = {
        'street_address': String(),
        'city': String(),
        'state': String(),
        'country': String(),
        'ext_code': Integer()
    }
    web_url = String()
    id_ = String()
    public = Boolean()
    for_profit = Boolean()
    degree = Boolean()
    other_names = String()

    def save(self, **kwargs):
        self.meta.id = self.id_
        return super(Institution, self).save(**kwargs)

    class Meta:
        index = ELASTIC_INST_INDEX