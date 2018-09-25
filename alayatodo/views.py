from alayatodo import app
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    flash,
    jsonify
    )


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
    if user:
        session['user'] = dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    cur = g.db.execute("SELECT * FROM todos")
    todos = cur.fetchall()
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    
    description = request.form.get('description', '')
    if not description:
        flash_message = 'You shoud provide a description'
    else:
        g.db.execute(
            "INSERT INTO todos (user_id, description) VALUES ('%s', '%s')"
            % (session['user']['id'], description)
        )
        g.db.commit()
        flash_message = 'Successfully added the new todo item'

    flash(flash_message)
    return redirect('/todo')


def _todo_get(id):
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    todo = cur.fetchone()
    return todo

@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    todo=_todo_get(id)
    return render_template('todo.html', todo=todo)    

@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    todo=_todo_get(id)
    return jsonify(dict(todo))


@app.route('/todo/<id>/delete', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute("DELETE FROM todos WHERE id ='%s'" % id)
    g.db.commit()
    return redirect('/todo')

@app.route('/todo/<id>/update', methods=['POST'])
def todo_mark_as_complete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    completed = int(request.form.get('completed'))
    g.db.execute("UPDATE todos SET completed = %s WHERE id ='%s'" % (completed, id))
    g.db.commit()

    flash_message = 'Successfully marked todo item ' + str(id) + ' as '
    flash_message += 'Complete' if completed == 1 else 'Incomplete'
    flash(flash_message)

    redirect_to = request.form.get('redirect_to');
    if not redirect_to:
        redirect_to = '/todo'
    return redirect(redirect_to)