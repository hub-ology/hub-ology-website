from flask.ext.login import login_required
from flask.ext.login import current_user

from hubology import app, templated
from hubology.models import HubUser

PAGESIZE = 25

@app.route('/people', methods=['GET'], defaults={'page':1})
@app.route('/people/<int:page>', methods=['GET'])
@templated()
@login_required
def people(page):
    users = HubUser.all()
    return dict(current_user=current_user, users=users, page=page)
    
@app.route('/people/json', methods=['GET'])
@templated('people.json')
@login_required
def people_json():
    """  Need to come up with a better way to get User info to client for mapping, etc.
    """
    users = HubUser.all_with_location()
    return dict(users=users)
