"""Renders signature pages for signatures from L1000FWD.
"""
import json
from flask import Blueprint, jsonify, redirect, request, render_template, \
    url_for, abort, make_response
from flask.ext.login import login_required

from gen3va.database import Drug, load_graphs_meta
from gen3va.config import Config
from gen3va import database
from gen3va.database import mongo, Signature


signature_pages = Blueprint('signature_pages',
                         __name__,
                         url_prefix=Config.SIG_URL)

@signature_pages.before_app_first_request
def get_globals():
    global graphs 
    graphs = load_graphs_meta()
    return

@signature_pages.route('/<string:sig_id>', methods=['GET'])
def view_signature(sig_id):
    """Landing page for the drug-induced signature.
    """
    sig = Signature(sig_id, mongo)

    drug = database.get(Drug, sig.pert_id, 'pert_id')

    return render_template('pages/signature.html',
                            sig=sig,
                            drug=drug,
                            graphs=graphs
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


@signature_pages.route('/binary/<string:sig_id>', methods=['GET'])
def signature_api(sig_id):
    """Get up/down gene sets:
    json encoded signature object: {up_genes: [], down_genes: [], sig_id: sig_id}.
    """
    sig = Signature(sig_id, mongo)
    sig_doc = {'sig_id': sig_id, 'up_genes': sig.upGenes, 'down_genes': sig.dnGenes}
    return json.dumps(sig_doc)

    