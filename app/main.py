from fastapi import FastAPI

app = FastAPI(title='Discountify Service - Code Challenge')


@app.get('/', include_in_schema=False)
def get_root():
    return {'message': 'Hello, World!'}
