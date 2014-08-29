PARTY
=====
Python client for the Artifactory API
----
## Usage

### Key Points
* Configuration is pre-loaded from ```party_config.py```, but can be overridden at runtime
* A new class must first be instantiated
* Any properties returned from using a "find" or "get" method are assigned to the class instance
* Properties are NOT appended. To add multiple properties to a class, get them all in one call.

Some example code:

```python
import party

artifact = party.Party()

artifact.artifactory_url = "http://myserver.com/api"  # <= Runtime config change

####  FIND ARTIFACT BY NAME
myFile = "my-file.rpm"
result = artifact.find(myFile)

####  FIND ARTIFACT BY PROPERTIES
file_props = {
    "build.number": 999,
    "rpm.version": "1.0.0.999"
}
result = artifact.find_by_properties(file_props)

####  FIND ARTIFACT BY PATTERN
result = artifact.find_by_pattern("erlang*R15B*.rpm")

####  GET SPECIFIC ARTIFACT PROPERTIES
specific_properties = [ "build.number", "rpm.version" ]
result = artifact.get_properties(artifact, specific_properties)

####  SET PROPERTIES ON AN ARTIFACT
new_properties = {
    "myKey": "myValue"
}
result = artifact.set_properties(artifact, new_properties)
```

## Configuring Party

Party class instances load in the values from ```party_config.py```. However, those values can be overridden directly in the file, or at runtime using:

```python
    artifact = party.Party()
    artifact.CONFIG_KEY = "new value"
```

The following is a list of config keys (CONFIG_KEY above) and descriptions of their purposes:

```
artifactory_url - Base URL to your Artifactory instance.
    search_prop - Artifactory API endpoint used for the property search.
    search_name - Artifactory API endpoint to access quick search.
   search_repos - Artifactory API endpoint to search for repositories.
       username - Username credential to use to connect to the Artifactory instance.
       password - Base64 encoded password credential used to connect to the Artifactory instance.
        headers - JSON (Python dict) of headers to send in the Artifactory queries.
```

## Methods

* All methods return ```None``` if the query returns an empty result, and ``OK`` if there were results. Successfully retrieved values are accessible as members of the class instance. 

* When specifying multiple properties, all successfully found properties will become members of the class instance. Missing properties are discarded, unless all queried properties don't exist, in which case ```None``` is returned.

----

#### find
**Description:** Find an artifact by filename.<br/>
**Produces:** (String) Instance variables "uri" and "name".<br/>
**Usage:** ```find(String)```<br/>
**Sample Output:**<br/>

```python
{
    u'results': [ {
        u'uri': u'http://my-server/artifactory/api/storage/libs-snapshot-local/com/mycompany/api/my-artifact/1.0.0-SNAPSHOT/my-artifact-1.0.0.999-1.noarch.rpm'
    } ]
}
```
#### find_by_properties
**Description:** Find an artifact by its properties.<br/>
**Produces:** (String) Instance variables "uri" and "name".<br/>
**Usage:** ```find_by_properties(Dict)```. Any number of properties can be specified within the dict.<br/>
**Sample Output:**

```python
{
    u'results': [ {
        u'uri': u'http://my-server/artifactory/api/storage/libs-snapshot-local/com/mycompany/api/my-artifact/1.0.0-SNAPSHOT/my-artifact-1.0.0.999-1.noarch.rpm'
    } ]
}
```

#### find_by_pattern
**Description:** Find an artifact by partial filename.<br/>
**Produces:** (List) Instance variable "files".<br/>
**Usage:** ```find_by_pattern(String, String, String, Int)```. See Parameters.<br/>
**Parameters:** ```find_by_pattern(filename, specific_repo, repo_type, max_depth):```
    - _filename_       - Required. Filename or partial filename to search.
    - _specific_repo_  - Optional. Specify an existing repository in Artifactory. When set to "None", it searches all repos (default).
    - _repo_type_      - Optional. Type of repository to search. Valid values are 'local', 'remote', 'virtual', or 'None'.
    - _max_depth_      - Optional. Number of directories deep to traverse to find the artifact.
**Sample Output:**

```python
[
    u'http://my-server/artifactory/api/storage/libs-snapshot-local/com/mycompany/api/my-artifact/1.0.0-SNAPSHOT/my-artifact-1.0.0.999-1.noarch.rpm'
]
```

#### get_properties
**Description:** Get specific properties from an artifact. <br/>
**Produces:** Class instance members of any found properties, referenced by specified keys.<br/>
**Usage:** ```get_properties(String, Dict)```. Any number of properties can be specified within the dict. Designed to be used in conjunction with the find methods to produce the filename.<br/>
**Sample Output:**

```python
{
    u'properties': {
        u'build.number': [u'537'],
        u'rpm.version': [u'4.2.1.537']
    },
    u'uri': u'http://my-server/artifactory/api/storage/libs-snapshot-local/com/mycompany/api/my-artifact/1.0.0-SNAPSHOT/my-artifact-1.0.0.999-1.noarch.rpm/'
}
```

#### set_properties
**Description:** Set specific properties on an artifact. **NOTE:** This will not set properties on your current class instance. Properties set using this method must be subsequently retrieved using the ```get_properties``` method.<br/>
**Produces:** HTTP status code. Return code of 204 is successful.<br/>
**Usage:** ```set_properties(String, Dict)```. Any number of properties can be specified within the dict. Please refer to http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html for a description of status codes.<br/>
**Sample Output:**

```
200
```
