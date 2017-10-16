"""Renders signature pages for signatures from L1000FWD.
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

@signature_pages.route('/download/<string:sig_id>/<string:direction>', methods=['GET'])
def download_gene_list(sig_id, direction):
    """Generate txt file for gene lists in gene signatures.
    direction should be attr name in one of ('combined_genes', 'up_genes', 'down_genes')
    """
    sig = Signature(sig_id, mongo)
    if direction == 'up_genes':
        gene_list = sig.upGenes
    elif direction == 'down_genes':
        gene_list = sig.dnGenes
    else:
        gene_list = sig.combined_genes

    # Make a file on-the-fly
    gene_list = '\n'.join(gene_list)
    filename = '%s-%s.txt' % (sig_id, direction)

    response = make_response(gene_list)
    response.headers["Content-Disposition"] = "attachment; filename=%s" % filename
    return response


    