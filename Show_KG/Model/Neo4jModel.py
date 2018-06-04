from py2neo import Graph,Node
import json
import sys

from Show_KG.Model import RelationNode


class Neo4jModel():
    graph = None
    def __init__(self):
        print("create neo4j class....")

    def connectDB(self):
        print("connect...")
        self.graph = Graph('http://localhost:7474/db/noe4jDatabase/',username='neo4j',password='123')
        print(self.graph)

    def query_brother_node(self):
        rel = self.graph.data("MATCH (source)-[r:`兄弟姐妹`]->(target) RETURN source.name,target.name")
        line_list = []
        for line in rel:
            line_list.append(json.loads(str(line).replace("'","\""),object_hook=RelationNode.dict2relation))
        return line_list

    def query_super_node(self):
        rel = self.graph.data("MATCH (source)-[r:`上下级`]->(target) RETURN source.name,target.name")
        line_list = []
        for line in rel:
            line_list.append(json.loads(str(line).replace("'","\""),object_hook=RelationNode.dict2relation))
        return line_list

    def query_cooperation_node(self):
        rel = self.graph.data("MATCH (source)-[r:`合作`]->(target) RETURN source.name,target.name")
        line_list = []
        print(rel)
        for line in rel:
            line_list.append(json.loads(str(line).replace("'","\""),object_hook=RelationNode.dict2relation))
        return line_list

    def query_node(self,name,relStr):
        rel = self.graph.data("MATCH (source{name:\""+name+"\"})-[r:`"+relStr+"`]-(target) RETURN source.name,target.name")
        line_list = []
        for line in rel:
            line_list.append(json.loads(str(line),object_hook=RelationNode.dict2relation))
        return line_list