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

	def __init__(self, sig_id, mongo, pvalue='SCS_centered_by_batch'):
		self.sig_id = sig_id
		doc = mongo.db.sigs.find_one({'sig_id':sig_id}, self.projection)

		for key, value in doc.items():
			value = self.dtypes.get(key, lambda x:x)(value)
			if key == pvalue:
				setattr(self, 'pvalue', value)
			else:
				setattr(self, key, value)

	def __repr__(self):
		return '<Signature %r>' % self.sig_id
