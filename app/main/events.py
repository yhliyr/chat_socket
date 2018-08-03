# @Time    : 2018/8/1 上午7:00
# @Author  : idri
# @File    : events.py
# @Software: PyCharm
from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from db import Rdb

db = Rdb()

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = message['msg']
    join_room(room)
    session['room'] = room

    msg = '<' + session.get('name') + ' has entered the room-{}. {}'.format(room, message['time']) + '>\n'
    db.save(room, msg)
    msg = (db.get_msg(room)).decode()
    emit('status', {'msg': msg}, room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    print("room", session.get("room"))
    room = message.get('room')
    msg = session.get('name') + ' '+ message['time']+'\n' + message['msg']
    emit('message', {'msg': msg}, room=room)
    db.save(room, msg)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    session.pop('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)
