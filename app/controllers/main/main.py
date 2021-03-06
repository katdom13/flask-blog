from flask import (
        render_template,
        redirect,
        url_for,
        Blueprint,
        flash,
        request,
        abort
    )

from flask_login import (
        login_required,
        current_user,
        login_user,
        logout_user
    )

from lib import password_encrypt, password_decrypt, generate_random_password, upload_file
from app.forms import AccountForm, PostForm
from app.models import Account, Post
from app.lib import BlogEmail
from urllib.parse import urljoin

main = Blueprint('main', __name__)

# ======================== PAGES =========================

@main.route('/login')
def login_page():
    if(current_user.is_authenticated and current_user.is_active):
        return redirect(url_for('main.home'))
    else:
        return render_template('/pages/login.html')


@main.route('/dashboard')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.get_all_posts(page=page)
    return render_template('/pages/home.html', posts=posts)


@main.route('/about')
def about():
    return render_template('/pages/about.html')


@main.route('/recover')
def recover_account_page():
    return render_template('/pages/recover.html')


@main.route('/reset/<reset_token>')
def reset_password_page(reset_token):
    account = Account.deserialize_token(reset_token)
    form = AccountForm(obj=account)

    if account:
        return render_template('/pages/reset.html', form=form, reset_token=reset_token, account=account)

    flash('Token is invalid!', 'danger')
    return redirect(url_for('main.login_page'))


@main.route('/<username>')
def posts(username):
    account = Account.find(username)

    if not account:
        abort(404, '')

    page = request.args.get('page', 1, type=int)
    posts = account.get_posts(page=page)
    return render_template('/pages/posts.html', account=account, posts=posts)


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
            return redirect(url_for('main.home'))
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
        return redirect(url_for('main.home'))

    form = AccountForm(request.form)

    if form.validate_on_submit():
        account = Account()
        form.populate_obj(account)

        account.password = password_encrypt(account.password)

        account.save()

        if login_user(account) and account.is_active():
            account.update_activity_tracking(request.remote_addr)
            return redirect(url_for('main.home'))

    return render_template('/pages/signup.html', form=form)


@main.route('/recover', methods=['POST'])
def recover_account():
    account = Account.find(request.form.get('identity'))

    if account:
        reset_token = account.serialize_token()
        BlogEmail.send_password_recovery_email(account, reset_token)

        return redirect(url_for('main.recover_account'))

    flash('Account does not exist', 'danger')
    return redirect(url_for('main.login_page'))


@main.route('/reset/<reset_token>', methods=['POST'])
def reset_password(reset_token):
    account = Account.deserialize_token(reset_token)
    form = AccountForm(obj=account)

    if account and form.validate_on_submit():
        account.password = password_encrypt(request.form.get('password'))
        account.save()

        flash('Password has been reset', 'success')
        return redirect(url_for('main.login_page'))

    flash('An error occurred', 'danger')
    return redirect(url_for('main.login_page'))


@main.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm(request.form)

    if form.validate_on_submit():
        post = Post()
        form.populate_obj(post)
        post.account_id = current_user.id
        post.save()

        return redirect(url_for('main.home'))

    return render_template('/pages/write_post.html', form=form)


@main.route('/post/<post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.find(post_id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)
        post.save()

        return redirect(url_for('main.home'))

    return render_template('/pages/write_post.html', form=form, post=post)


@main.route('/post/<post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    post = Post.find(post_id)
    if post:
        post.delete()

    return redirect(url_for('main.home'))


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

    return render_template('/pages/read_post.html', form=form, post=post)


@main.route('/upload_picture', methods=['POST'])
@login_required
def upload():

    if 'profile-pic-input' not in request.files:
        flash('No image uploaded', 'danger')
        return redirect(url_for('main.error_page'))

    image_file = request.files.get('profile-pic-input')

    if image_file:
        directory = upload_file(image_file, user=current_user)
        current_user.profile_pic = directory
        current_user.save()
        return redirect(url_for('main.profile'))

    flash('An Error occurred', 'danger')
    return redirect(url_for('main.profile'))


@main.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = AccountForm(obj=current_user)

    if form.validate_on_submit():
        if password_decrypt(request.form.get('old_password'), current_user.password):
            current_user.password = password_encrypt(request.form.get('password'))
            current_user.save()
            flash('Password changed succesfully', 'success')
        else:
            flash('Entered password does not match your current password', 'danger')
    else:
        flash('Password was not changed', 'danger')

    return redirect(url_for('main.profile'))
