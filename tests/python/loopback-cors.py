from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from flask import Flask
from flask_cors import CORS

app = FastAPI()

# The mnemo-cortex shape before 4.27.0.
# ruleid: python-cors-allows-any-origin
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def build(config):
    origins = config.get("cors_origins", ["*"])
    api = FastAPI()
    # ruleid: python-cors-allows-any-origin
    api.add_middleware(CORSMiddleware, allow_origins=origins)
    return api


# ok: python-cors-allows-any-origin
app.add_middleware(CORSMiddleware, allow_origins=["http://127.0.0.1:5173"], allow_methods=["*"])


def build_fixed(config):
    origins = config.get("cors_origins", [])
    api = FastAPI()
    if origins:
        # ok: python-cors-allows-any-origin
        api.add_middleware(CORSMiddleware, allow_origins=origins)
    return api


# ruleid: python-cors-origin-regex-matches-anything
app.add_middleware(CORSMiddleware, allow_origin_regex=".*")
# ruleid: python-cors-origin-regex-matches-anything
app.add_middleware(CORSMiddleware, allow_origin_regex=r"^https?://.*$")
# ok: python-cors-origin-regex-matches-anything
app.add_middleware(CORSMiddleware, allow_origin_regex=r"^https://([a-z]+\.)?example\.com$")

flask_app = Flask(__name__)
# ruleid: python-flask-cors-default-any-origin
CORS(flask_app)
# ok: python-flask-cors-default-any-origin
CORS(flask_app, origins=["http://localhost:3000"])
# ruleid: python-cors-allows-any-origin
CORS(flask_app, origins="*")
