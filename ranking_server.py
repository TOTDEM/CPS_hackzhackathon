# Import necessary modules from FastAPI, pydantic, and CORS
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from fastapi.middleware.cors import CORSMiddleware # CORSミドルウェアをインポート

# Initialize the FastAPI application
app = FastAPI(
    title="User Score Accumulator API",
    description="A simple FastAPI server to accumulate and manage scores for multiple users.",
    version="1.0.0"
)

# --- CORS (Cross-Origin Resource Sharing) 設定 ---
# 開発中はすべてのオリジンからのアクセスを許可するために "*" を使用します。
# 本番環境では、セキュリティのため、特定のオリジン（例: ["http://localhost", "http://localhost:8080"]）を指定することを強く推奨します。
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "null",  # file:// プロトコルでHTMLを開く場合に必要になることがあります
    "*" # すべてのオリジンを許可（開発目的でのみ推奨）
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # 許可するオリジンを指定
    allow_credentials=True, # クッキーや認証ヘッダーを許可するかどうか
    allow_methods=["*"], # 許可するHTTPメソッド (GET, POSTなど)
    allow_headers=["*"], # 許可するHTTPヘッダー
)


# --- In-memory Data Storage ---
# This dictionary will store user scores.
# The key will be the user_id (string) and the value will be the score (integer).
# Note: Data stored this way is ephemeral and will be lost when the server restarts.
user_scores: Dict[str, int] = {}

# --- Pydantic Models for Request and Response Bodies ---

class ScoreUpdate(BaseModel):
    """
    Pydantic model for updating a user's score.
    score: The amount to add to the user's current score. Can be positive or negative.
    """
    score: int

class UserScore(BaseModel):
    """
    Pydantic model for representing a user's score in responses.
    user_id: The unique identifier for the user.
    score: The current score of the user.
    """
    user_id: str
    score: int

class MessageResponse(BaseModel):
    """
    Pydantic model for general success/error messages.
    message: A descriptive message about the operation.
    """
    message: str

# --- API Endpoints ---

@app.post("/users/{user_id}/add", response_model=MessageResponse)
async def add_user(user_id: str):
    """
    Adds a new user with an initial score of 0 if they don't already exist.
    """
    if user_id in user_scores:
        raise HTTPException(status_code=409, detail=f"User '{user_id}' already exists.")
    user_scores[user_id] = 0
    return {"message": f"User '{user_id}' added with initial score 0."}

@app.post("/users/{user_id}/score", response_model=UserScore)
async def update_user_score(user_id: str, score_update: ScoreUpdate):
    """
    Updates the score for a specific user.
    If the user does not exist, they will be added with the provided score.
    """
    if user_id not in user_scores:
        user_scores[user_id] = 0 # Initialize if not exists
        print(f"User '{user_id}' not found. Initializing score to 0 before update.")

    user_scores[user_id] += score_update.score
    return {"user_id": user_id, "score": user_scores[user_id]}

@app.get("/users/{user_id}/score", response_model=UserScore)
async def get_user_score(user_id: str):
    """
    Retrieves the current score for a specific user.
    Raises a 404 error if the user is not found.
    """
    if user_id not in user_scores:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found.")
    return {"user_id": user_id, "score": user_scores[user_id]}

@app.get("/users", response_model=List[UserScore])
async def get_all_users_scores():
    """
    Retrieves a list of all users and their current scores.
    """
    return [{"user_id": user_id, "score": score} for user_id, score in user_scores.items()]

# --- How to run the server ---
# To run this server, you would typically save it as a Python file (e.g., test_server.py)
# and then run the following command in your terminal:
# uvicorn ranking_server:app --reload --port 8000
#
# You will need to install FastAPI, Uvicorn, and python-multipart first:
# pip install fastapi uvicorn python-multipart
