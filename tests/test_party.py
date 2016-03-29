import party
from flexmock import flexmock
from nose.tools import assert_equals, assert_raises, assert_is_instance, set_trace
import json
import base64

#== USER INPUTS
testprops = {"build.number": "789"}


def test_artifact_object_structure():
    """ The Artifact object is structured as expected. """
    artifact = party.Party()
    # The 'files' property is a list
    assert_is_instance(artifact.files, list)


def test_loading_config_values():
    """ __init__: Configuration values load properly and are set as object attributes. """

    pass


def test_find_by_properties_pass():
    """ find_by_properties: We can find an artifact by using properties. """

    artifact = party.Party()

    #== SET UP: GOOD MOCK OBJECT
    mock_json_good = json.dumps({"results": [{"uri": "file-name.rpm"}]})
    mock_response_good = flexmock(status_code=200, text=mock_json_good)

    flexmock(artifact).should_receive(
        "query_artifactory").and_return(mock_response_good)

    # Method returns properly?
    assert_equals(artifact.find_by_properties(testprops), "OK")
    # Files are set properly in the object?
    assert_equals(artifact.files, ["file-name.rpm"])
    # Object has the correct returned file count?
    assert_equals(artifact.count, 1)


def test_find_by_properties_fail():
    """ find_by_properties: Handles list of zero files as expected. """

    artifact = party.Party()

    flexmock(artifact).should_receive("query_artifactory").and_return(None)
    # Method returns None?
    assert_equals(artifact.find_by_properties(testprops), None)
    # File list doesn't exist?
    assert_equals(artifact.files, [])
    # Object has no attribute named "count?"
    with assert_raises(AttributeError):
        assert_equals(artifact.count, 0)


def test_find_by_pattern_pass():
    """ find_by_pattern: We can find an artifact by using a pattern. """
    artifact = party.Party()
    mock_repo_uri = "http://mock"
    mock_file_list = ["file1.rpm", "file2.rpm"]
    mock_uris = [
        "%s/%s" % (mock_repo_uri, mock_file_list[0]),
        "%s/%s" % (mock_repo_uri, mock_file_list[1])
    ]
    mock_json_good = json.dumps(
        {"repoUri": mock_repo_uri, "files": mock_file_list})
    mock_response_good = flexmock(status_code=200, text=mock_json_good)

    flexmock(artifact).should_receive(
        "query_artifactory").and_return(mock_response_good)
    flexmock(artifact).should_receive(
        "get_repositories").and_return({"key": "mock-repo-local"})

    # Ensure artifact.files has spliced filenames
    artifact.find_by_pattern("none", None, None, 1)
    assert_equals(artifact.files, mock_uris)


def test_find_by_pattern_fail():
    """ find_by_pattern: Handles exceptions as expected. """
    artifact = party.Party()
    mock_json_bad = json.dumps({"repoUri": "", "files": []})
    mock_response_bad = flexmock(status_code=404, text=[])

    flexmock(artifact).should_receive(
        "query_artifactory").and_return(mock_response_bad)

    # Ensure ValueError is raised for no filename
    with assert_raises(ValueError):
        artifact.find_by_pattern("")

    # Ensure repotype matches a valid value
    with assert_raises(ValueError):
        artifact.find_by_pattern("filename", None, "nope")


def test_get_repositories():
    """ get_repositories: Returns a list of repositories. """
    artifact = party.Party()
    mock_json_good = json.dumps([{"key": "mykey"}])
    mock_response_good = flexmock(status_code=200, text=mock_json_good)
    flexmock(artifact).should_receive(
        "query_artifactory").and_return(mock_response_good)

    repos = artifact.get_repositories("local")
    assert_is_instance(repos, list)
    assert_equals(repos, ["mykey"])
