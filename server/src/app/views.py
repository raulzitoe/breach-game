from datetime import datetime

from . import app, socketio, game_manager

from flask import render_template
from flask_socketio import emit, join_room

from flask import session
from flask import request


@app.route("/", methods=['GET', 'POST'])
def home():
    game_state = {}
    if request.method == 'POST':
        if request.form["action"] == "create_game":
            game_state = game_manager.create_game()
            session['game_id'] = game_state['game_id']
            # todo: is this safe because its serverside session? 
            # so maybe this doesn't allow player to change curren_player?
            session['current_player'] = 'player1'
        elif request.form["action"] == "end_game":
            session.clear()
        elif request.form["action"] == "join_game":
            game_state = game_manager.join_game(request.form["token"])

            if game_state:
                session['game_id'] = game_state['game_id']
                session['current_player'] = 'player2'
    else:
        if 'game_id' in session:
            game_state = game_manager.get_board(session['game_id'])

    return render_template("index.html", session=session, post_data=request.form, game_state=game_state)

@socketio.on('connect')
def connect():
    if 'game_id' in session:
        join_room(session['game_id'])

@socketio.on('next_pos')
def next_pos(message):
    if message['action'] == 'left':
        # todo: check if game id and current_player exist
        new_pos = game_manager.move_left(session['game_id'], session['current_player'])
    elif message['action'] == 'right':
        new_pos = game_manager.move_right(session['game_id'], session['current_player'])
    
    emit('update_status', 
                {f"{session['current_player']}_pos": new_pos}, 
                room=session['game_id'])