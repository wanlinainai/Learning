from enum import Enum

from fastapi import FastAPI

app = FastAPI()

# 如果路径存在重复；比如下述的都是/user开始，第一个是输入，第二个是固定，
# 如果我们输入/user/me，访问的是第一个接口，所以需要自己规划好接口的顺序


# @app.get("/user/{item_name}")
# async def read_user_name(item_name: str):
#     return {"name": item_name}

@app.get("/user/me")
async def read_user_me():
    return {"user_id": "Current_user"}

@app.get("/user/{item_name}")
async def read_user_name(item_name: str):
    return {"name": item_name}



# 枚举类
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name.value == ModelName.alexnet:
        return {"model_name": "AlexNet", "message": "Hello, AlexNet."}
    elif model_name.value == ModelName.resnet:
        return {"model_name": "ResNet", "message": "Hello, ResNet."}

    return {"model_name": "LeNet", "message": "Hello, LeNet."}