"""Serves menu pages.
"""

import json

from flask import abort, Blueprint, render_template, request

from substrate import BioCategory, Curator, Tag
from gen3va.database import Drug
from gen3va.database import database
from gen3va.config import Config


menu_pages = Blueprint('menu_pages',
                       __name__,
                       url_prefix=Config.BASE_URL)


# Main pages
# ----------------------------------------------------------------------------

# @menu_pages.route('/', methods=['GET'])
# def index():
#     curator_name = request.args.get('curator')
#     if curator_name:
#         bio_categories = database.get_bio_categories_by_curator(curator_name)
#         # We don't need to show the curator when the user has already elected
#         # to see only signatures by a specific curator.
#         curators = None
#     else:
#         bio_categories = database.get_bio_categories()
#         curators = _curators_with_approved_reports()
#     bio_category_names = json.dumps([cat.name for cat in bio_categories])
#     return render_template('index.html',
#                            curators=curators,
#                            curator_name=curator_name,
#                            bio_category_names=bio_category_names,
#                            bio_categories=bio_categories)

@menu_pages.before_app_first_request
def get_globals():
    global tags, d_pert_name
    tags = database.get_all(Tag)
    d_pert_name = _get_pertid_names(tags)
    print len(tags), len(d_pert_name)
    return

@menu_pages.route('/', methods=['GET'])
def collections():
    return render_template('pages/collections.html',
                           tags=tags,
                           d_pert_name=d_pert_name,
                           menu_item='collections')


@menu_pages.route('/get-started', methods=['GET'])
def get_started():
    return render_template('pages/get-started.html',
                           menu_item='get-started')


@menu_pages.route('/upload/<string:type_>', methods=['GET'])
def upload(type_):
    if type_ == 'combined':
        return render_template('pages/upload-combined.html',
                               menu_item='upload')
    elif type_ == 'up-down':
        return render_template('pages/upload-up-down.html',
                               menu_item='upload')
    else:
        abort(404)


@menu_pages.route('/documentation', methods=['GET'])
def documentation():
    return render_template('pages/documentation.html',
                           menu_item='documentation')


@menu_pages.route('/statistics', methods=['GET'])
def statistics():
    stats = database.get_statistics()
    stats_json = json.dumps(stats)
    return render_template('pages/statistics.html',
                           stats=stats,
                           stats_json=stats_json,
                           menu_item='stats')


# Utility methods
# ----------------------------------------------------------------------------

def _curators_with_approved_reports():
    """Returns curators that have at least one ready report.
    """
    curators = []
    for curator in database.get_all(Curator):
        use = False
        for tag in curator.tags:
            if tag.approved_report and tag.approved_report.ready:
                use = True
        if use:
            curators.append(curator)
    return curators

def _get_pertid_names(tags):
  """Returns a dict with pert_id as key and pert_iname as value.
  """
  tag_names = map(lambda x:x.name, tags)
  drugs = database.get_many(Drug, tag_names, 'pert_id')
  d = {drug.pert_id: drug.pert_iname for drug in drugs}
  return d
