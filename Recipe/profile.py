from flask import Blueprint, g, render_template, request, redirect, url_for, flash
from Recipe.db import get_db
from Recipe.auth import login_required

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/<username>')
@login_required
def view(username):
    db = get_db()
    user = db.execute(
        'SELECT id, username, email, university FROM user WHERE username = ?',
        (username,)
    ).fetchone()

    if user is None:
        flash("User not found.")
        return redirect(url_for('recipe.index'))

    recipes = db.execute(
        'SELECT id, title, created FROM recipe WHERE author_id = ? ORDER BY created DESC',
        (user['id'],)
    ).fetchall()

    return render_template('profile/profile.html', user=user, recipes=recipes)


@bp.route('/<username>/edit', methods=('POST',))
@login_required
def edit(username):
    username = request.form['username']
    email = request.form['email']
    university = request.form['university']

    db = get_db()

    try:
        db.execute(
            'UPDATE user SET username = ?, email = ?, university = ? WHERE id = ?',
            (username, email, university, g.user['id'])
        )
        db.commit()
    except db.IntegrityError:
        flash('That username is already taken.', 'error')
        return redirect(url_for('profile.view', username=g.user['username']))

    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile.view', username=username))
