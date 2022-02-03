import os

from flask import Flask
from flask_cors import CORS

from routes import register as register_http
from queries import register as register_graphql

from ariadne import load_schema_from_path, make_executable_schema, ObjectType

# Create Application
app = Flask(__name__)
CORS(app)

# Map GraphQL Resolvers
query = ObjectType("Query")
register_graphql(query)

# Load Schema
type_defs = load_schema_from_path(
    f"{os.path.dirname(os.path.abspath(__file__))}/schema.graphql"
)
schema = make_executable_schema(type_defs, query)

# Map HTTP Resolvers
register_http(app, schema)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
