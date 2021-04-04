# wikibase-sync

Python library to synchronise data between RDF files and Wikibase instances.

It updates your wikibase instance based on the changes of the RDF ontology.

## Examples
With the following code you can synchronize the modification of two RDF files to a given Wikibase instance:
```python
from wbsync.triplestore import WikibaseAdapter
from wbsync.synchronization import GraphDiffSyncAlgorithm, OntologySynchronizer

mediawiki_api_url='wikibase_api_endpoint'
sparql_endpoint_url='wikibase_sparql_endpoint'
username='wikibase_username'
password='wikibase_password'
adapter = WikibaseAdapter(mediawiki_api_url, sparql_endpoint_url, username, password)

algorithm = GraphDiffSyncAlgorithm()
synchronizer = OntologySynchronizer(algorithm)

source_content = "original rdf content goes here"
target_content = "final rdf content goes here"
ops = synchronizer.synchronize(source_content, target_content)
for op in ops:
    res = op.execute(adapter)
    if not res.successful:
        print(f"Error synchronizing triple: {res.message}")
```

Leaving the source_content empty will be equivalent to adding the target contents to the Wikibase, while leaving the target_content empty will be equivalent to removing the source_content from the Wikibase if present. Additional examples about synchronizing RDF files with a Wikibase instance can be seen in the [Synchronization notebook](notebooks/Synchronization.ipynb).

## Executing batch operations
There is the possibility of performing batch operations (executing at once all of the statements of a given entity). This type of synchronization will have a better performance at the risk that an invalid statement will cancel the entire batch operation. The following code can be used to execute batch operations:
```python
from wbsync.synchronization.operations import optimize_ops

def execute_batch_synchronization(source_content, target_content, synchronizer, adapter):
    ops = synchronizer.synchronize(source_content, target_content)
    batch_ops = optimize_ops(ops)
    for op in batch_ops:
        res = op.execute(adapter)
        if not res.successful:
            print(f"Error synchronizing triple: {res.message}")
```

More information about these operations and time gained with them can be explored in the [Benchmarks notebook](notebooks/Benchmarks.ipynb).
