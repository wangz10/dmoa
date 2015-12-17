"""Performs PCA on a list of gene signatures or a SOFT file.
"""


from flask import Blueprint, render_template, request, jsonify
import json

from gen3va.db import commondal
from gen3va.core.pca import pca
from gen3va.config import Config


pca_api = Blueprint('pca_api',
                    __name__,
                    url_prefix=Config.BASE_URL + '/pca')


@pca_api.route('', methods=['POST'])
def perform_gene_signatures_pca():
    """Performs PCA on a list of gene signatures, referenced by extraction_id.
    """
    pca_data = pca.from_gene_signatures(request.json)
    return jsonify(pca_data)


@pca_api.route('/<extraction_id>', methods=['GET'])
def perform_soft_file_pca(extraction_id):
    """Performs PCA on a SOFT file, referenced by extraction_id.
    """
    gene_signature = commondal.fetch_gene_signature(extraction_id)
    if gene_signature:
        pca_data = pca.from_soft_file(gene_signature.soft_file)
        pca_json = json.dumps(pca_data)
        return render_template('pca.html',
                               pca_data=pca_json,
                               results_url=Config.BASE_RESULTS_URL,
                               extraction_id=gene_signature.extraction_id)