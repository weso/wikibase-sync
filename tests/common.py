import os

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'synchronization')

def load_file_from(source, target):
    with open(os.path.join(DATA_DIR, source), 'r') as f:
        source_content = f.read()
    with open(os.path.join(DATA_DIR, target), 'r') as f:
        target_content = f.read()
    return source_content, target_content
