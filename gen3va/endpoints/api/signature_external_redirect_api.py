"""
Implement using signatures to other tools such as L1000CDS2 to redirect to result page.  
"""
import json
import requests
from flask import Blueprint, redirect, abort

from substrate import OptionalMetadata, GeneSignature
from gen3va import database
from gen3va.config import Config


signature_external_redirect_api = Blueprint('signature_external_redirect_api',
                         __name__,
                         url_prefix='%s/redirect' % Config.BASE_URL)

@signature_external_redirect_api.route('/L1000CDS2/<sig_id>', methods=['GET'])
def post_to_l1000cds2(sig_id):
	"""POST signature to L1000CDS2 API, then redirect to the result page.
	"""
	# get GeneSignature instance
	gene_signature_fk = database.get(OptionalMetadata, sig_id, 'value').gene_signature_fk
	gene_signature = database.get(GeneSignature, gene_signature_fk, 'id')
	# retrieve up_genes, down_genes
	up_genes = [rg.gene.name for rg in gene_signature.up_genes]
	down_genes = [rg.gene.name for rg in gene_signature.down_genes]
	# POST to L1000CDS2
	cds2_url = 'http://amp.pharm.mssm.edu/L1000CDS2/query'
	data = {'upGenes': up_genes, 'dnGenes': down_genes}
	config = {"aggravate":True,"searchMethod":"geneSet","share":True,"combination":False,"db-version":"latest"}
	metadata = [{"key":"sig_id","value":sig_id}]
	payload = {"data":data,"config":config,"meta":metadata}
	headers = {'content-type':'application/json'}

	resp = requests.post(cds2_url, data=json.dumps(payload), headers=headers)
	if resp.status_code == 200:
		resp = resp.json()
		share_id = resp['shareId']
		result_url = 'http://amp.pharm.mssm.edu/L1000CDS2/#/result/%s' % share_id
		return redirect(result_url)
	else:
		abort(404)

