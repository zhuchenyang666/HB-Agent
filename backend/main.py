from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"Msg": "Hello"}


if __name__ == '__main__':
    pass
