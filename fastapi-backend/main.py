from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.mount('/images', StaticFiles(directory='images'), name='images')

redis = get_redis_connection(
    host='redis-12580.c290.ap-northeast-1-2.ec2.cloud.redislabs.com',
    port=12580,
    password='C2Kwd3fifwJInzDCCTsWRpaXh4xGcdWv',
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.post('/product')
def create(product: Product):
    return product.save()


@app.get('/product/{pk}')
def get(pk: str):
    return Product.get(pk)


@app.get('/products')
def all():
    # return Product.all_pks()
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.delete('/product/{pk}')
def delete(pk: str):
    return Product.delete(pk)
