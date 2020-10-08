import os, sys
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
from app.db.dbo.baseclass import Base
target_metadata = Base.metadata

from sqlalchemy_schemadisplay import create_schema_graph
# create the pydot graph object by autoloading all tables via a bound metadata object
graph = create_schema_graph(metadata=target_metadata)
graph.write_png('dbschema.png') # write out the file
