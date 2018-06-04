import sys
import json
from Show_KG.Model.Neo4jModel import Neo4jModel
from Show_KG.Model import RelationNode

class KGService():
    neo4j = None
    def __init__(self):
        pass
    def init(self):
        print('init neo4j')
        self.neo4j = Neo4jModel()
        self.neo4j.connectDB()
    def query_brother_node(self):
        return json.dumps(self.neo4j.query_brother_node(),default=RelationNode.relation2dict,ensure_ascii=False)

    def query_super_node(self):
        return json.dumps(self.neo4j.query_super_node(),default=RelationNode.relation2dict,ensure_ascii=False)

    def query_cooperation_node(self):
        return json.dumps(self.neo4j.query_cooperation_node(),default=RelationNode.relation2dict,ensure_ascii=False)

    def query_node(self,name,rel):
        return json.dumps(self.neo4j.query_node(name,rel),default=RelationNode.relation2dict,ensure_ascii=False)

