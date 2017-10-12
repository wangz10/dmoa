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

	def __repr__(self):
		return '<Signature %r>' % self.sig_id
