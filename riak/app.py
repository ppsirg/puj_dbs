from riak import RiakClient, RiakNode

RiakClient()
RiakClient(protocol='http', host='127.0.0.1', http_port=8098)
RiakClient(nodes=[{'host':'127.0.0.1','http_port':8098}])
RiakClient(protocol='http', nodes=[RiakNode()])