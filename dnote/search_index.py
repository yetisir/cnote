from whoosh import fields, analysis, qparser, index
from whoosh.filedb import filestore

schema = fields.Schema(
    id=fields.ID(stored=True),
    text=fields.TEXT(stored=True, analyzer=analysis.StemmingAnalyzer()),
    timestamp=fields.NUMERIC(),
    tags=fields.KEYWORD(),
)


storage = filestore.RamStorage()
index = storage.create_index(schema)


writer = index.writer()
writer.add_document(
    id='123451234',
    text='This is the second document as a matter of fact bitches',
    timestamp=23452395,
    tags = ['greasy', 'broccolli'],
)
writer.add_document(
    id='12341234',
    text='This is the first docuemnt full text but what can we do?',
    timestamp=23452345,
    tags = ['greasy', 'select', 'plaid', 'groovy', 'broccolli'],
)

writer.commit()

with index.searcher() as searcher:
    query = qparser.QueryParser('text', index.schema).parse('document')
    results = searcher.search(query)
    print(results[0])

