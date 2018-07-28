from threading import Lock
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from models import recipes
from device import get_weight
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


thread = None
thread_lock = Lock()


def get_weight_socketio():
    weight = 0
    while True:
        socketio.sleep(0.5)
        if app.debug:
            import random
            weight = random.randint(5, 100)
        else:
            weight = get_weight() or weight
        socketio.emit('weight', weight)


def set_timer_task(timer):
    for i in range(timer, -1, -1):
        socketio.emit('timer', i)
        socketio.sleep(1)


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
    context = dict(
        current_step=step_id + 1,
        max_step=1 + len(recipe.procedures),
        recipe=recipes.get(rid),
        procedure=current_procedure,
    )
    return render_template('procedure.html', **context)


@app.route('/next', methods=['POST'])
def next():
    socketio.emit('next-btn')
    return 'ok'


@app.route('/reset', methods=['POST'])
def reset():
    socketio.emit('reset-btn')
    return 'ok'


@app.route('/debug/weight/<weight>')
def debug_weight(weight: str):
    if app.debug:
        weight = int(weight)
        import random
        for i in range(10):
            socketio.emit('weight', random.randint(max(0, weight - 10), weight + 10))
            socketio.sleep(0.25)
    return 'ok'


@app.route('/timer', methods=['POST'])
def set_timer():
    timer = request.form['timer']
    timer = int(timer)
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(
                target=set_timer_task, **dict(timer=timer))
    return 'ok'


@socketio.on('connect')
def on_connect():
    if app.debug:
        return
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=get_weight)


if __name__ == '__main__':
    socketio.run(app)
