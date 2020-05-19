from flask import redirect, url_for
from app.config import app
from app.controllers.main import main


# =================== Blueprints ===================
app.register_blueprint(main)

# ======================== PAGES =========================
@app.route('/')
def start():
    return redirect(url_for('main.signup'))
