import os
import sqlite3
from flask import Flask, g, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'blog.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'dev-secret-key'  # 在真實專案請用安全的方式管理


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    cur = db.cursor()
    # posts includes author column so we can show personal homepage
    cur.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        image TEXT,
        author TEXT,
        author_id INTEGER,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        author TEXT NOT NULL,
        content TEXT NOT NULL,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE
    )''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        name TEXT,
        bio TEXT,
        photo TEXT
    )''')
    # users table for authentication
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        name TEXT,
        bio TEXT,
        photo TEXT
    )''')
    # ensure single profile row exists
    cur.execute("INSERT OR IGNORE INTO profile (id, name, bio, photo) VALUES (1, '', '', '')")
    db.commit()


def ensure_posts_author_column():
    # ensure legacy DB has author column
    db = get_db()
    cur = db.execute("PRAGMA table_info(posts)")
    cols = [r['name'] for r in cur.fetchall()]
    if 'author' not in cols:
        db.execute('ALTER TABLE posts ADD COLUMN author TEXT')
        db.commit()
    # ensure author_id exists
    colnames = cols
    if 'author_id' not in colnames:
        try:
            db.execute('ALTER TABLE posts ADD COLUMN author_id INTEGER')
            db.commit()
        except Exception:
            pass


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(fn):
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login', next=request.path))
        return fn(*args, **kwargs)

    return wrapper


def get_current_user():
    uid = session.get('user_id')
    if not uid:
        return None
    db = get_db()
    cur = db.execute('SELECT id, username, name, bio, photo FROM users WHERE id = ?', (uid,))
    return cur.fetchone()


@app.before_request
def before_request():
    # ensure DB exists
    db_missing = False
    if not os.path.exists(DATABASE):
        db_missing = True
    else:
        # check whether 'users' table exists; if not, we should initialize schema
        try:
            db = get_db()
            cur = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if cur.fetchone() is None:
                db_missing = True
        except Exception:
            db_missing = True

    if db_missing:
        try:
            init_db()
        except Exception:
            # if initialization fails, ignore here and let the route show the error
            pass
    # ensure posts table has author column for older DBs
    try:
        ensure_posts_author_column()
    except Exception:
        # ignore if DB not ready
        pass


@app.route('/')
def index():
    # If user is logged in, show their personal blog (profile + their posts) on HOME
    user = get_current_user()
    db = get_db()
    if user:
        # fetch posts authored by this user (match by username or author_id)
        cur = db.execute('SELECT id, title, content, image, created FROM posts WHERE author = ? OR author_id = ? ORDER BY created DESC', (user['username'], user['id']))
        posts = cur.fetchall()
        return render_template('profile_home.html', profile=user, posts=posts)

    # default: show global feed
    cur = db.execute('SELECT id, title, content, image, created FROM posts ORDER BY created DESC')
    posts = cur.fetchall()
    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_view(post_id):
    db = get_db()
    if request.method == 'POST':
        author = request.form.get('author', 'Anonymous')
        content = request.form.get('content', '').strip()
        if not content:
            flash('留言內容不能為空')
            return redirect(url_for('post_view', post_id=post_id))
        db.execute('INSERT INTO comments (post_id, author, content) VALUES (?, ?, ?)',
                   (post_id, author, content))
        db.commit()
        return redirect(url_for('post_view', post_id=post_id))

    cur = db.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = cur.fetchone()
    if post is None:
        return 'Post not found', 404
    cur2 = db.execute('SELECT author, content, created FROM comments WHERE post_id = ? ORDER BY created ASC', (post_id,))
    comments = cur2.fetchall()
    return render_template('post.html', post=post, comments=comments)


@app.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    db = get_db()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            flash('標題與內容為必填')
            return redirect(url_for('new_post'))
        filename = None
        file = request.files.get('image')
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_" + file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user = get_current_user()
        author = user['username'] if user else 'Anonymous'
        author_id = user['id'] if user else None
        db.execute('INSERT INTO posts (title, content, image, author, author_id) VALUES (?, ?, ?, ?, ?)', (title, content, filename, author, author_id))
        db.commit()
        return redirect(url_for('index'))
    # pre-fill profile name if logged in
    user = get_current_user()
    profile_name = user['name'] if user and user['name'] else ''
    return render_template('new_post.html', profile_name=profile_name)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    db = get_db()
    user = get_current_user()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        bio = request.form.get('bio', '').strip()
        file = request.files.get('photo')
        photo = None
        if file and file.filename != '' and allowed_file(file.filename):
            photo = secure_filename(f"profile_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_" + file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo))
        # update user row
        if photo:
            db.execute('UPDATE users SET name = ?, bio = ?, photo = ? WHERE id = ?', (name, bio, photo, user['id']))
        else:
            db.execute('UPDATE users SET name = ?, bio = ? WHERE id = ?', (name, bio, user['id']))
        db.commit()
        return redirect(url_for('profile'))

    cur = db.execute('SELECT name, bio, photo FROM users WHERE id = ?', (user['id'],))
    prof = cur.fetchone()
    return render_template('profile.html', profile=prof)


@app.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash('請填寫使用者名稱與密碼')
            return redirect(url_for('register'))
        cur = db.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cur.fetchone():
            flash('使用者名稱已存在')
            return redirect(url_for('register'))
        ph = generate_password_hash(password)
        db.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, ph))
        db.commit()
        flash('註冊完成，請登入')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        cur = db.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
        row = cur.fetchone()
        if row and check_password_hash(row['password_hash'], password):
            session.clear()
            session['user_id'] = row['id']
            flash('登入成功')
            next_url = request.args.get('next')
            return redirect(next_url or url_for('index'))
        flash('登入失敗')
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('已登出')
    return redirect(url_for('index'))


@app.route('/user/<username>')
def user_profile(username):
    db = get_db()
    cur = db.execute('SELECT id, username, name, bio, photo FROM users WHERE username = ?', (username,))
    user = cur.fetchone()
    if not user:
        return 'User not found', 404
    cur2 = db.execute('SELECT id, title, content, image, created FROM posts WHERE author = ? ORDER BY created DESC', (username,))
    posts = cur2.fetchall()
    return render_template('profile_home.html', profile=user, posts=posts)


@app.route('/me')
def my_home():
    db = get_db()
    cur = db.execute('SELECT name, bio, photo FROM profile WHERE id = 1')
    prof = cur.fetchone()
    name = prof['name'] if prof and prof['name'] else None
    posts = []
    if name:
        cur2 = db.execute('SELECT id, title, content, image, created FROM posts WHERE author = ? ORDER BY created DESC', (name,))
        posts = cur2.fetchall()
    return render_template('profile_home.html', profile=prof, posts=posts)


if __name__ == '__main__':
    # ensure DB created
    if not os.path.exists(DATABASE):
        with app.app_context():
            init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)
