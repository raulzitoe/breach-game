from flask import Flask
from flask_redis import FlaskRedis
from flask_socketio import SocketIO
from flask_session import Session
from .game_logic import GameManager
from uuid import uuid4

app = Flask(__name__)
app.config['SECRET_KEY'] = uuid4().hex
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["REDIS_URL"] = "redis://redis:6379"
Session(app)

redis_client = FlaskRedis(app)
game_manager = GameManager(redis_client)

# manage_session is by default true and that's ok
# because we no longer change the session inside
# a socket request
# TODO: remove cors_allowed_origins
socketio = SocketIO(app, manage_session=True, logger=True, engineio_logger=True, cors_allowed_origins="*")