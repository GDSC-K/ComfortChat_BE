import json

from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import database
import scheme
from model import Account, Chat
from util import gpt_util
import crud

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.redirect_slashes = False


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/hello")
async def root():
    return {"message": "Hello! We are ComfortChat!"}


@app.post("/chats/text")
async def add_chat(req: scheme.ChatCreateTextReq, db: Session = Depends(get_db)):
    response = json.loads(gpt_util.get_gpt_answer(question=req.question))
    print(response)
    chat = crud.create_chat(db=db, chat=Chat(
        question=req.question,
        answer=response["answer"],
        keyword=response["keyword"],
        isOkay=response["isOkay"]
    ))

    return scheme.ChatResponse(
        id=chat.id,
        question=chat.question,
        answer=chat.answer,
        isOkay=chat.isOkay,
        keyword=chat.keyword
    )
