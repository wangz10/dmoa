'''
Handles connections to MongoDB and ORMs.
'''

from flask_pymongo import PyMongo

mongo = PyMongo()

class Signature(object):
	"""Signature object in the MongoDB."""

	projection = {
		'_id': False,
		'avg_center_LM': False,
		'CD_nocenter_LM': False,
		'avg_center_LM_det': False,
		'CDavg_center_LM_det': False,
		'CDavg_nocenter_LM_det': False,
		'CD_center_Full': False,
		'pvalues_Full':False,
		'sigIdx': False,
	}

	dtypes = {
		'pert_time': int,
	}

	collections = {
		# map for finding which collection to look for the signature
		3: ('sigs', 'SCS_centered_by_batch'),
		2: ('sigs_pert_cell', 'avg_pvalue'),
		1: ('sigs_pert', 'avg_pvalue'),
	}

	def __init__(self, sig_id, mongo):
		self.sig_id = sig_id
		coll_name, pvalue = self.collections[len(sig_id.split(':'))]

		doc = mongo.db[coll_name].find_one({'sig_id':sig_id}, self.projection)
		if coll_name == 'sigs_pert':
			doc['pert_id'] = sig_id

		for key, value in doc.items():
			value = self.dtypes.get(key, lambda x:x)(value)
			if key == pvalue:
				setattr(self, 'pvalue', value)
			else:
				setattr(self, key, value)

		# Get combined_genes
		self.combined_genes = list(set(doc.get('upGenes', [])) | set(doc.get('dnGenes', [])))

	def __repr__(self):
		return '<Signature %r>' % self.sig_id


def load_graphs_meta():
	'''Load and preprocess the meta for graphs in the `graphs` collection.
	'''
	graph_names = mongo.db.graphs.distinct('name')
	graphs = {
		'cells':[
			{'name': 'Signature_Graph_CD_center_LM_sig-only_16848nodes.gml.cyjs', 'display_name': 'All cell lines'}
		],
		'agg': [
			{'name': 'graph_pert_cell_12894nodes_99.9.gml.cyjs', 'display_name': 'Aggregated by drugs and cells'},
			{'name': 'kNN_5_layout', 'display_name': 'Aggregated by drugs (kNN)'},
			{'name': 'threshold_99.5', 'display_name': 'Aggregated by drugs (thresholding)'},
		],
	}

	# process graphs for individual cells
	for graph_name in graph_names:
		if graph_name.endswith('-tSNE_layout.csv'):
			cell = graph_name.split('-')[0]
			rec = {
				'name': graph_name, 
				'display_name': '%s (tSNE)' % cell
				}
			graphs['cells'].append(rec)

		elif graph_name.endswith('kNN_5'):
			cell = graph_name.split('_')[0]
			rec = {
				'name': graph_name,
				'display_name': '%s (kNN)' % cell
			}
			graphs['cells'].append(rec)
	return graphs
