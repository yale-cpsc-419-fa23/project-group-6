from flask import Blueprint, jsonify, request, render_template, redirect, flash, current_app, url_for, session

from app.models.user import User

user = Blueprint('user', __name__)


@user.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id=None):
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        user_id = request.json.get('user_id')

    if not user_id:
        flash('No user ID provided.', 'danger')
        return redirect(url_for('main.home'))

    user = User.find_by_id(user_id)
    user_id1 = session.get("user_id")
    user1 = User.find_by_id(user_id1)
    is_following = user1.is_following(user_id)
    liked_songs_records = user.create_records
    created_songs = []
    for record in liked_songs_records:
        song = record.song
        upload_date = record.UploadDate
        creators = song.get_creators_profiles()
        created_songs.append((song, upload_date, creators))
    return render_template('user_profile.html',
                           user=user,
                           songs=created_songs,
                           is_following=is_following)


@user.route('/follow', methods=['POST'])
def follow():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('auth.login'))

    user_id = session.get("user_id")
    user = User.find_by_id(user_id)
    user_id2 = request.json.get('user_id')
    if user.follow(user_id2):
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Already followed"}), 400


@user.route('/unfollow', methods=['POST'])
def unfollow():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('auth.login'))

    user_id = session.get("user_id")
    user = User.find_by_id(user_id)
    user_id2 = request.json.get('user_id')
    if user.unfollow(user_id2):
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Already unfollowed"}), 400
