from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware


from typing import Optional
from pydantic import BaseModel

from views_predct import ModelHolder, InputManager, PredScore

# set a target variable
y_n = "открытия материала"
# choose dataset
data_path = "ved_5mon_sent_n_o.csv"

# a model and iput interpreter
holder = ModelHolder(data_path, y_n)
inputs = InputManager(data_path)

# a varable to hold predictions and labels
pred_score = PredScore(-1)

app = FastAPI()


origins = [
    'http://localhost:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class Article(BaseModel):
    title: Optional[str] = Form(None)
    authors: Optional[str] = Form(None)
    topics: Optional[str] = Form(None)

# receive data from react and make a prediction
@app.post("/api")
async def root(article: Article):
    inps = inputs.return_as_pd_df(article.title, article.authors, article.topics)
    pred = holder.predict(inps)[0]

    print(pred)
    pred_score.update(pred)
    print(pred_score.label)
    return {"prediction":pred}

# give prediction data to react
@app.get("/api")
async def get_pred():
    return {"score":int(pred_score.score), "label":pred_score.label}
