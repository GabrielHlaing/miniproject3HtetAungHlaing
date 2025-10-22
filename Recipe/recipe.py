from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from Recipe.db import get_db
from Recipe.auth import login_required

bp = Blueprint('recipe', __name__)

# --- Show all recipes ---
@bp.route('/')
def index():
    db = get_db()
    recipes = db.execute(
        'SELECT r.id, title, body, created, author_id, username'
        ' FROM recipe r JOIN user u ON r.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('recipe/index.html', recipes=recipes)


# --- Create a new recipe ---
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO recipe (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('recipe.index'))

    return render_template('recipe/create.html')


# --- Helper: Get a recipe by ID ---
def get_recipe(id, check_author=True):
    recipe = get_db().execute(
        'SELECT r.id, title, body, created, author_id, username'
        ' FROM recipe r JOIN user u ON r.author_id = u.id'
        ' WHERE r.id = ?',
        (id,)
    ).fetchone()

    if recipe is None:
        abort(404, f"Recipe id {id} doesn’t exist.")

    if check_author and recipe['author_id'] != g.user['id']:
        abort(403)

    return recipe


# --- View a single recipe ---
@bp.route('/<int:id>')
def detail(id):
    recipe = get_recipe(id, check_author=False)
    return render_template('recipe/detail.html', recipe=recipe)


# --- Update/Edit a recipe ---
@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    recipe = get_recipe(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE recipe SET title = ?, body = ? WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('recipe.index'))

    return render_template('recipe/edit.html', recipe=recipe)


# --- Delete a recipe ---
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_recipe(id)
    db = get_db()
    db.execute('DELETE FROM recipe WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('recipe.index'))


# --- User Profile Page ---
@bp.route('/profile/<username>')
def profile(username):
    db = get_db()
    user = db.execute(
        'SELECT id, username FROM user WHERE username = ?',
        (username,)
    ).fetchone()

    if user is None:
        abort(404, f"User '{username}' not found.")

    recipes = db.execute(
        'SELECT id, title, created FROM recipe WHERE author_id = ? ORDER BY created DESC',
        (user['id'],)
    ).fetchall()

    return render_template('recipe/profile.html', user=user, recipes=recipes)
