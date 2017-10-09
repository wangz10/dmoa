"""Renders signature pages.
"""

from flask import Blueprint, jsonify, redirect, request, render_template, \
    url_for, abort, make_response
from flask.ext.login import login_required

from gen3va.database import Drug
from gen3va.config import Config
from gen3va import database
from gen3va.database import mongo, Signature


signature_pages = Blueprint('signature_pages',
                         __name__,
                         url_prefix=Config.SIG_URL)

@signature_pages.route('/<string:sig_id>', methods=['GET'])
def view_signature(sig_id):
    """Landing page for the drug-induced signature.
    """
    print sig_id
    # sig = mongo.db.sigs.find_one({'sig_id': sig_id}, {'_id':False})
    sig = Signature(sig_id, mongo)
    print sig.pvalue

    drug = database.get(Drug, sig.pert_id, 'pert_id')

    return render_template('pages/signature.html',
                            sig=sig,
                            drug=drug
                            )

