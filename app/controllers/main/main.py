from flask import (
        render_template,
        redirect,
        url_for,
        Blueprint,
        flash,
        request
    )

from flask_login import (
        login_required,
        current_user,
        login_user,
        logout_user
    )

from lib import password_encrypt, password_decrypt, generate_random_password
from app.forms import AccountForm, PostForm
from app.models import Account, Post
from urllib.parse import urljoin

main = Blueprint('main', __name__)

# ======================== PAGES =========================

@main.route('/login')
def login_page():
    if(current_user.is_authenticated and current_user.is_active):
        return redirect(url_for('main.home_page'))
    else:
        return render_template('/pages/login.html')


@main.route('/dashboard')
@login_required
def home_page():
    return render_template('/pages/home.html')


# ======================= METHODS ========================


@main.route('/login', methods=['POST'])
def login():
    account = Account.find(request.form.get('identity'))
    if account and password_decrypt(request.form.get('password'), account.password):
        if account.is_active() and login_user(account, remember=True):
            account.update_activity_tracking(request.remote_addr)
            next_url = request.args.get('next')
            if next_url:
                return redirect(urljoin(request.host_url, next_url))
            return redirect(url_for('main.home_page'))
        else:
            flash('That account is disabled', 'danger')
    else:
        flash('Identity or password is incorrect', 'danger')

    return redirect(url_for('main.login_page'))


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login_page'))


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if(current_user.is_authenticated and current_user.is_active):
        return redirect(url_for('main.home_page'))

    form = AccountForm(request.form)

    if form.validate_on_submit():
        account = Account()
        form.populate_obj(account)

        account.password = password_encrypt(account.password)

        account.save()

        if login_user(account) and account.is_active():
            account.update_activity_tracking(request.remote_addr)
            return redirect(url_for('main.home_page'))

    return render_template('/pages/signup.html', form=form)


@main.route('/create', methods=['GET', 'POST'])
def create():
    form = PostForm(request.form)

    if form.validate_on_submit():
        post = Post()
        form.populate_obj(post)

        post.save()

        return redirect(url_for('main.home_page'))

    return render_template('/pages/write_post.html', form=form)


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = AccountForm(obj=current_user)

    if form.validate_on_submit():
        form.populate_obj(current_user)
        current_user.save()

        return(redirect(url_for('main.profile')))

    return render_template('/pages/profile.html', form=form)


@main.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    form = PostForm(request.form)
    post = Post.find(post_id)

    if form.validate_on_submit():
        form.populate_obj(post)
        post.save()

        return redirect(url_for('main.post', post_id=post.id))

    return render_template('/pages/post.html', form=form, post=post)
