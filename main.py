#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2020/09/09 23:47:15
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicso@wicos.cn
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Blog    :   https://www.wicos.me
'''

# here put the import lib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from pydantic import BaseModel
from model import trans
import json

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def jsonX(jsonfile):
    with open(jsonfile,'rb') as fp:
        a = json.load(fp)
    return a
MYCONFIG = jsonX("config.json")
TRANS = trans.Trans(MYCONFIG["fanyi"]["appid"],MYCONFIG["fanyi"]["secretKey"])

class Item(BaseModel):
    q:str
    fromlang:str = None
    tolang:str
    domain:str

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})

@app.post("/fanyi")
async def fanyi(item:Item):
    #print(Fy)
    get_dict = item.dict()
    print(get_dict)
    bc = TRANS.start_trans(get_dict["q"],tolang=get_dict["tolang"],domain=get_dict["domain"],fromlang=get_dict["fromlang"])
    return bc