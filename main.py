from threading import Lock
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from models import recipes
from device import init_hx711, get_weight, get_next_btn
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

hx711 = init_hx711()


thread = None
thread_lock = Lock()


def get_weight_socketio():
    weight = 0
    while True:
        socketio.sleep(0.2)
        if app.debug:
            import random
            weight = random.randint(5, 100)
        else:
            new_weight = get_weight(hx711)
            weight = new_weight if new_weight is not None else weight
        socketio.emit('weight', weight)


def get_next_btn_socketio():
    if app.debug:
        return
    while True:
        if get_next_btn():
            socketio.emit('next-btn')
            socketio.sleep(1)


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
    if step_id > len(recipe.procedures):
        return redirect(url_for('top'))
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
    with thread_lock:
        socketio.start_background_task(
            target=set_timer_task, **dict(timer=timer))
    return 'ok'


@app.route('/speech', methods=['POST'])
def speech():
    import os
    content = request.form['content']
    if content != ":STOP:":
        print('say {}'.format(content))
        os.system("./AquesTalkPi '{}'| aplay".format(content))
    else:
        print('stop speech')
        os.system("pkill -f aplay")
    return 'ok'


@socketio.on('connect')
def on_connect():
    if app.debug:
        return
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=get_weight_socketio)
            thread = socketio.start_background_task(target=get_next_btn_socketio)


if __name__ == '__main__':
    socketio.run(app)
