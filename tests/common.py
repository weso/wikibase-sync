import os
from rdfsync.wb2rdf.conversion import Converter

converter = Converter(endpoint='', input_format='ttl')

MEDIAWIKI_API_URL = "https://wikibase-sync-test.wikibase.cloud/w/api.php"
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'synchronization')

def load_file_from(source, target):
    with open(os.path.join(DATA_DIR, source), 'r') as f:
        source_content = f.read()
    with open(os.path.join(DATA_DIR, target), 'r') as f:
        target_content = f.read()
    return source_content, target_content

def load_graph_from(source):
    return converter.read_file_and_create_graph('tests/data/synchronization/' + source)
