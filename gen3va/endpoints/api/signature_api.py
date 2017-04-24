"""
API endpoint for retrieving up/down genes or CD vector of signatures given sig_id.
"""
import json
import requests
from flask import Blueprint

from substrate import OptionalMetadata, GeneSignature
from gen3va import database
from gen3va.config import Config


signature_api = Blueprint('signature_api',
                         __name__,
                         url_prefix='%s/signature' % Config.BASE_URL)


@signature_api.route('/binary/<sig_id>', methods=['GET'])
def get_binary(sig_id):
	"""Get up/down gene sets.
	"""
	# get GeneSignature instance
	gene_signature_fk = database.get(OptionalMetadata, sig_id, 'value').gene_signature_fk
	gene_signature = database.get(GeneSignature, gene_signature_fk, 'id')
	# retrieve up_genes, down_genes
	up_genes = [rg.gene.name for rg in gene_signature.up_genes]
	down_genes = [rg.gene.name for rg in gene_signature.down_genes]
	return json.dumps({'up_genes': up_genes, 'down_genes': down_genes, 'sig_id': sig_id})

@signature_api.route('/all', methods=['GET'])
def get_all_signatures_meta():
	"""Get the metadata for all signatures.
	"""
	sig_ids = database.get_many(OptionalMetadata, ['sig_id'], 'name')
	sig_ids = [sig_id.value for sig_id in sig_ids]
	return json.dumps({'sig_ids': sig_ids})

