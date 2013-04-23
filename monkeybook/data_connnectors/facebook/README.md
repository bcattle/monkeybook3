The `FacebookConnector` class holds a collection of `Connectors`. 
* A `Connector` encapsulates a particular call we can make to the FB server, for instance `ProfileFieldsConnector`
returns a subset of the fields from a user's profile. 

`ProfileFieldsConnector` is a subclass of `FqlConnector`, which contains the general logic for making a generic FQL query. 

`ProfileFieldsConnector.run()` returns a `ResultsCollection` object, which is a list of `ProfileFieldsResult` classes.

Each resource is paired with a custom subclass of `ConnectorResult`, defining the list of fields that are returned from 
that query. 
* Fields can be required, in which case a BlankFieldError will be raised if the field is not returned from the server.
* Design decision: it is not possible to specify the _default value_ of a field here. The rationale is that the 
`FacebookConnector` is responsible only for connecting to the server and raising an error for server-related errors 
(unable to connect, schema incorrect). Manipulating the schema is a "consumption" step best handled elsewhere. 

The base class `ConnectorResult` handles the actual logic of validating that all required fields are present. 
