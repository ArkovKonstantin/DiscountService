from graphene import ObjectType, String, Int, List, Schema
import random
import grpc
import helloworld_pb2
import helloworld_pb2_grpc

class Product(ObjectType):
    id = Int()
    name = String()
    price = Int()
    discount = Int()

data = dict((i, Product(id=i, name=f'prod_{i}', discount=random.randint(5, 20)))
            for i in range(1, 6))

class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    product_list = List(Product)
    hello = String(name=String(default_value="stranger"))
    goodbye = String()

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_product_list(root, info):
        # request products price
        # grpc client
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = helloworld_pb2_grpc.GreeterStub(channel)
            # response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
            # print("Greeter client received: " + response.message)
            prices = stub.GetPrices(helloworld_pb2.PriceRequest(name='you'))
            print("data", data)
            for p in prices:
                data[p.id].price = p.price

        return data.values()

    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'


schema = Schema(query=Query)

# Querying

query_string = '{ hello(name:"Petya")' \
               '  goodbye' \
               ' }'
result = schema.execute(query_string)
print(result.data)
