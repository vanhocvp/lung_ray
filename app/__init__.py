
# import gevent.monkey
# gevent.monkey.patch_all()
from flask import Flask

from flask_socketio import SocketIO

from flask import Blueprint

from flask_session import Session
socketio = SocketIO()
main = Blueprint('main', __name__)
from . import routes, events
def create_app(debug = False):
    app = Flask(__name__)
    app.debug = debug
    app.register_blueprint(main)

    app.config['SECRET_KEY'] = 'vanhoc123@123'
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    socketio.init_app(app,cors_allowed_origins="*", manage_session=False)
    
    return app
