import sys, json, requests, urllib, base64, re, os
from party_config import party_config

class Party:

	def __init__(self):
		for k, v in party_config.iteritems():
			setattr(self, '%s' % (k,), v)

	def query_artifactory(self, query, query_type='get', payload=None):
		if query_type.lower() == "get":
			response = requests.get(query, auth=(self.username, base64.b64decode(self.password)), headers=self.headers)
		elif query_type.lower() == "put":
			response = requests.put(query, data=query.split('?',1)[1], auth=(self.username, base64.b64decode(self.password)), headers=self.headers)
		if query_type.lower() == "post":
			pass

		return response

	def find_by_properties(self, properties):
		"""
		Look up an artifact, or artifacts, in Artfiactory by
		using properties that have been set on the artifact.
		@param: properties - List of properties to use as search criteria.
		"""
		query = "%s/%s?%s" % (self.artifactory_url, self.search_prop, urllib.urlencode(properties))
		raw_response = self.query_artifactory(query)
		if raw_response.status_code is not 200:
			return None
		response = json.loads(raw_response.text)
		if len(response['results']) < 1:
			return None

		for item in response['results']:
			for k, v in item.iteritems():
				setattr(self, '%s' % (k,), v)

		artifact_list = [ ]
		for u in response['results']:
			artifact_list.append(os.path.basename(u['uri']))

		setattr(self, 'list', artifact_list)
		setattr(self, 'count', len(artifact_list))
		
		return "OK"


	def find(self, filename):
		"""
		Look up an artifact, or artifacts, in Artfiactory by
		its filename.
		@param: filename - Filename of the artifact to search.
		"""
		query = "%s/%s?name=%s" % (self.artifactory_url, self.search_name, filename)
		raw_response = self.query_artifactory(query)
		if raw_response.status_code is not 200:
			return None
		response = json.loads(raw_response.text)
		if len(response['results']) < 1:
			return None

		setattr(self, 'name', filename)
		setattr(self, 'url', response)

		return "OK"


	def get_properties(self, filename, properties=None):
		"""
		Get an artifact's properties, as defined in the Properties tab in
		Artifactory.
		@param: filename - Filename of artifact of which to get properties.
		@param: properties - Optional. List of properties to help filter results.
		"""
		if properties:
			query = "%s/?properties=%s" % (filename, ",".join(properties))
		else:
			query = "%s/?properties" % filename

		raw_response = self.query_artifactory(query)
		if raw_response.status_code == 404:
			return None
		response = json.loads(raw_response.text)
		for key, value in response.iteritems():
			setattr(self, '%s' % (key,), value)

		return "OK"


	def set_properties(self, file_url, properties):
		"""
		Set properties on an artifact.
		@param: file_url - URL of artifact on which to set properties.
		@param: properties - JSON list of properties to set on the artifact.
		"""
		query = "%s?properties=%s" % (file_url, urllib.urlencode(properties).replace('&', '|'))
		response = self.query_artifactory(query, "put")
		match = re.search(r'^20.*$', str(response.status_code))
		if not match:
			return None

		return "OK"
