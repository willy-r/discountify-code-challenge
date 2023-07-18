from fastapi import FastAPI

from app.api.routes import coupons

app = FastAPI(title='Discountify Service - Code Challenge')

# Routes
app.include_router(coupons.router)


@app.get('/', include_in_schema=False)
def read_root():
    return {'message': 'Hello, World!'}
