from neo4j import GraphDatabase
import nxneo4j as nx

driver = GraphDatabase.driver(uri="bolt://100.25.33.237:36845",auth=("neo4j","population-sets-field"))
config = {
    "node_label": "user",
    "relationship_type": None,
    "identifier_property": "unique_id"
}
G = nx.DiGraph(driver,config)
def create_user(details):
    # details=''
    G.add_node("{}".format(details['email'][:-10]),name=details['name'],
               phone=details['phone'],email=details['email'],password=details['password'])

def user_checker(email):
    try:
        a=G.nodes[email[:-10]]
        # print(a)
        return True
    except:
        return False

def get_user_details(email):
    user_detail=G.nodes[email[:-10]]
    return user_detail
# d={}
# m={}
# m['email']='zorogorilla@gmail.com'
# m['name']='zoro'
# m['phone']='8888888888'
# m['password']='123rohit'
# # d['sanjilove']=m
# print(str(d))

# create_user(m)
# for g in G.nodes(data=True):
#     print(g)
# user_checker('sanjiloe@gmail.com')