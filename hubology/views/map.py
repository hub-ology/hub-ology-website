from flask.ext.login import login_required, current_user
from hubology import app, templated

@app.route('/map')
@templated()
@login_required
def user_map():
    return {'current_user': current_user}