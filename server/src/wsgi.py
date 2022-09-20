from app import app, socketio    # For application discovery by the 'flask' command.
from app import views  # For import side-effects of setting up routes.

if __name__ == "__main__":
    socketio.run(app, debug=True)