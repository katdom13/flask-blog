from flask_login import current_user
from flask import Blueprint, render_template, request
from app.forms import AccountForm

div = Blueprint('div', __name__)


@div.route('/div/profile/<action>', methods=['GET'])
def profile(action):
    form = AccountForm(obj=current_user)
    return render_template('/divs/div-profile.html', action=action, form=form)
