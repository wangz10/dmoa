'''
Make some fake signatures and upload them to g2e API endpoint
'''
import json
import numpy as np

import pandas as pd
from sqlalchemy import create_engine
import requests

# to upload gene lists
G2E_API = 'http://127.0.0.1:8083/g2e/api/extract/upload_gene_list'

hgnc_genes = pd.read_csv('protein-coding_gene.txt', sep='\t').set_index('hgnc_id')
hgnc_genes = hgnc_genes[['symbol']]
print hgnc_genes.head()
genes = hgnc_genes['symbol'].tolist()

cells = ['MCF7', 'PC3', 'MCF10A']
doses = [1, 5, 10]
times = [6, 24]

def make_fake_signature(genes, n_genes=100):
	genes = np.random.choice(genes, n_genes, replace=False)
	vals = np.random.ranf(n_genes) - 0.5
	signature = zip(genes, vals)
	return signature



# make 5 fake drugs
engine = create_engine('mysql://root:@localhost/maaya0_SEP')
drugs_lincs = pd.read_sql('drugs_lincs', engine).set_index('pert_id')
print drugs_lincs.shape
print drugs_lincs.head()

c = 0
for pert_id, row in drugs_lincs.iterrows():
	c += 1
	print pert_id
	drug_name = row['pert_iname']
	structure_url = row['structure_url']
	# fake 10 signatures for each drug
	for i in range(10):
		sig = make_fake_signature(genes)
		cell = np.random.choice(cells, 1)[0]
		dose = np.random.choice(doses, 1)[0]
		time = np.random.choice(times, 1)[0]
		sig_id = '%s:%s_%s_%s' % (pert_id, cell, dose, time)
		payload = {
			'ranked_genes': sig,
			'diffexp_method': 'chdir',
			'tags': ['test_tag', pert_id],
			'gene': None,
			'cell': cell,
			'perturbation': drug_name,
			'disease': None,
			## optional metadata
			'metadata[pert_id]': pert_id,
			'metadata[dose]': dose,
			'metadata[time]': time,
			'metadata[sig_id]': sig_id,
		}
		resp = requests.post(G2E_API, data=json.dumps(payload))

	if c >2:
		break

