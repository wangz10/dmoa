"""Error handling.
"""


from flask import Blueprint
from gen3va.config import Config
from gen3va.database import load_graphs_meta
from gen3va import app
from flask import render_template


error_page = Blueprint('error_page',
                       __name__,
                       url_prefix=Config.BASE_URL)


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    graphs = load_graphs_meta()
    return render_template('pages/404.html', 
    	graphs=graphs)