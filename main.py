from threading import Lock
from flask import Flask, render_template
from flask_socketio import SocketIO
from models import recipes
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


thread = None
thread_lock = Lock()


def background_thread():
    while True:
        socketio.sleep(1)
        import time
        import random
        t = time.strftime('%M:%S', time.localtime())
        socketio.emit('server_response',
                      [{'type': 'button', 'data': 1}, {'type': 'weight', 'data': random.randint(0, 100)}],
                      namespace='/test')


@app.route('/')
def top():
    context = dict(
        recipes=recipes
    )
    return render_template('top.html', **context)


@app.route('/recipe/<int:rid>/ingredient')
def ingredient(rid: int):
    recipe = recipes.get(rid)
    context = dict(
        current_step=1,
        max_step=1 + len(recipe.procedures),
        recipe=recipes.get(rid),
        active_ri_idx=0,
    )
    return render_template('ingredient.html', **context)


@app.route('/recipe/<int:rid>/procedures/<int:step_id>')
def procedure(rid: int, step_id: int):
    recipe = recipes.get(rid)
    current_procedure = recipe.procedures[step_id - 1]
    try:
        next_procedure = recipe.procedures[step_id]
    except IndexError:
        next_procedure = None
    context = dict(
        current_step=step_id + 1,
        max_step=1 + len(recipe.procedures),
        recipe=recipes.get(rid),
        current_procedure=current_procedure,
        next_procedure=next_procedure
    )
    return render_template('procedure.html', **context)


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


if __name__ == '__main__':
    socketio.run(app)
