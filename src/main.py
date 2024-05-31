from v1.api import app
import uvicorn

if __name__ == '__main__':
    uvicorn.run(app, port=80, host='127.0.0.1')