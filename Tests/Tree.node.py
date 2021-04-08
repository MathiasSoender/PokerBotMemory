from Services.database_SQLite import DB
from Tree.node import Node
from Tree.Tree import Tree

db = DB()

a = db.get_node("root")
a.find_distribution(0.5)
