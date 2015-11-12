 
from model.model import Database, Project

Database.reset()

project = Project(name="thinksns",url="thinksns.com",description="for debug")
project.save()

