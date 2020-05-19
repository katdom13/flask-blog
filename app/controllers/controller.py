from flask import redirect, url_for, render_template
from app.config import app
from app.controllers.main import main

# =================== Blueprints ===================
app.register_blueprint(main)

# ======================== PAGES =========================
@app.route('/')
def start():
    return redirect(url_for('main.signup'))

@app.errorhandler(403)
def page_403(err):
    return render_template('/errors/403.html'), 403


@app.errorhandler(404)
def page_404(err):
    return render_template('/errors/404.html'), 404


@app.errorhandler(500)
def page_505(err):
    return render_template('/errors/500.html'), 500
