from fastapi import FastAPI

from app.core.settings import settings

app = FastAPI(title='Discountify Service - Code Challenge')

@app.get('/', include_in_schema=False)
def get_root():
    return {'message': 'Hello, World!'}
