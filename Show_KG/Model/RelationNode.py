class Relation():
    def __init__(self,source,target):
        self.source = source
        self.target = target



def relation2dict(rel):
    return {
        'source':rel.source,
        'target':rel.target
    }
def dict2relation(d):
    return Relation(d['source.name'],d['target.name'])