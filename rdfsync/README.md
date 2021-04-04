# rdfsync

An algorithm to synchronise data between the ontology files and a given Wikibase instance.

It updates an ontology file from the changes made in your Wikibase instance.

## How to synchronize

With the following code you can synchronize the modification of your ontology or rdf file with the updated given
Wikibase instance:

```python
from rdfsync.wb2rdf.conversion import Converter
from rdfsync.githubcon.github_connection import GithubConnection
from rdflib import Graph
import ntpath

# graph ops
file_path = FILE_PATH  # your rdf file path, required even if the file's empty

# algorithm execution
converter = Converter(endpoint=MEDIAWIKI_API_URL, input_format='ttl')  # (http|https)://XXX/w/api.php
converter.read_file_and_create_graph(file_path)  # creates a graph from the rdf file

# items_props_to_sync = {'P228', 'Q1', 'P10'} # if you know the items that changed
items_props_to_sync = converter.get_items_properties_to_sync()
for item_property in items_props_to_sync:
    converter.execute_synchronization(wb_id=item_property)  # synchronization

# if you want to create the file in a specific directory, UNCOMMENT THE FOLLOWING CODE
# final_graph = Graph()
# final_graph.parse(converter.serialize_file(output_format='ttl'))
# final_graph.serialize(FILE_DESTINATION, format='ttl', encoding='utf8')

# pushing the changes to github in a specific branch and pull request
github_token = GITHUB_ACCESS_TOKEN  # personalized github access token
repository_name = GITHUB_TARGET_REPO  # your github repository name
source_branch = SOURCE_BRANCH  # master or main
target_branch = TARGET_BRANCH  # your new branch name in order to create the PR

file_name = ntpath.basename(file_path)
file_content = converter.serialize_file()

gitcon = GithubConnection()
gitcon.update_github_repo(github_token=github_token, repository_name=repository_name, source_branch=source_branch,
                          target_branch=target_branch, file_name=file_name, file_content=file_content)

```

