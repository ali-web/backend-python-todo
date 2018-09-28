from alayatodo import app, db
from alayatodo.models import Todo, User
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    flash,
    jsonify
    )

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)

    return d    

def logged_in_user_id():
    user_id = session.get('user_id', None)
    return user_id


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    if logged_in_user_id():
        return redirect('/')    
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        dict_user = row2dict(user)
        session['user_id'] = dict_user['id']
        session['username'] = dict_user['username']
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect('/')


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    user_id = logged_in_user_id()
    if not user_id:
        return redirect('/login')

    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    page_size = 10

    todos = Todo.query.filter_by(user_id=user_id).paginate(page, page_size, False)
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    user_id = logged_in_user_id()
    if not user_id:
        return redirect('/login')
    
    description = request.form.get('description', '')
    if not description:
        flash_message = 'You shoud provide a description'
    else:
        todo = Todo(user_id, description, 0)
        db.session.add(todo)
        db.session.commit()
        flash_message = 'Successfully added the new todo item'

    flash(flash_message)
    return redirect('/todo')


def _todo_item(id):
    todo = Todo.query.filter_by(id=id, user_id=logged_in_user_id()).first_or_404()
    return todo

@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    if not logged_in_user_id():
        return redirect('/login')    
    todo = _todo_item(id)
    return render_template('todo.html', todo=todo)

@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    if not logged_in_user_id():
        return redirect('/login')    
    todo = _todo_item(id)
    return jsonify(row2dict(todo))


@app.route('/todo/<id>/delete', methods=['POST'])
def todo_delete(id):
    if not logged_in_user_id():
        return redirect('/login')
    todo = _todo_item(id)
    db.session.delete(todo)
    db.session.commit()

    flash_message = 'Successfully deleted todo item ' + str(id)
    flash(flash_message)    
    return redirect('/todo')

@app.route('/todo/<id>/update', methods=['POST'])
def todo_mark_as_complete(id):
    if not logged_in_user_id():
        return redirect('/login')
    completed = int(request.form.get('completed'))
    todo = _todo_item(id)   
    todo.completed = completed
    db.session.commit()

    flash_message = 'Successfully marked todo item ' + str(id) + ' as '
    flash_message += 'Complete' if completed == 1 else 'Incomplete'
    flash(flash_message)

    redirect_to = request.form.get('redirect_to');
    if not redirect_to:
        redirect_to = '/todo'
    return redirect(redirect_to)