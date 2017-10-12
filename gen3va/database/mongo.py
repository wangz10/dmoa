'''
Handles connections to MongoDB and ORMs.
'''
import os
import json, requests
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from sqlalchemy import create_engine
from bson.objectid import ObjectId
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

## Loaders for metadata and graphs
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


def load_signature_meta_from_db(collection_name, query={}, drug_meta_df=None):
	projection = {
		'_id': False,
		'batch': False,
		'avg_center_LM': False,
		'CD_nocenter_LM': False,
		'CD_center_LM': False,
		'avg_center_LM_det': False,
		'CDavg_center_LM_det': False,
		'CDavg_nocenter_LM_det': False,
		'CD_center_LM_det': False,
		'distil_id':False,
		}
	coll = mongo.db[collection_name]
	cur = coll.find(query, projection)
	print cur.count()
	meta_df = pd.DataFrame.from_records([doc for doc in cur]).set_index('sig_id')
	if collection_name == 'sigs_pert':
		meta_df['pert_id'] = meta_df.index

	meta_df = meta_df.rename(index=str, columns={'cell_id':'cell','pert_dose':'dose'})
	if drug_meta_df is not None:
		meta_df = meta_df.merge(drug_meta_df, 
			left_on='pert_id', 
			right_index=True,
			how='left'
			)
	meta_df.fillna('unknown', inplace=True)
	meta_df.replace(['unannotated', '-666'], 'unknown', inplace=True)
	print meta_df.shape
	return meta_df


def _minmax_scaling(arr):
	scl = MinMaxScaler((-10, 10))
	arr = scl.fit_transform(arr.reshape(-1, 1))
	return arr[:, 0]

def load_graph_from_db(graph_name, drug_meta_df=None):
	# Find the graph by name
	graph_doc = mongo.db.graphs.find_one({'name': graph_name}, {'_id':False})
	graph_df = pd.DataFrame({
		'sig_ids': graph_doc['sig_ids'],
		'x': graph_doc['x'],
		'y': graph_doc['y'],
		}).set_index('sig_ids')
	graph_df.index.name = 'sig_id'
	# Scale the x, y 
	graph_df['x'] = _minmax_scaling(graph_df['x'].values)
	graph_df['y'] = _minmax_scaling(graph_df['y'].values)
	graph_df['z'] = 0

	# Load the corresponding meta_df
	meta_df = load_signature_meta_from_db(graph_doc['coll'], 
		query={'sig_id': {'$in': graph_df.index.tolist()}},
		drug_meta_df=drug_meta_df
		)

	graph_df = graph_df.merge(meta_df, how='left', left_index=True, right_index=True)
	# Check form of sig_id
	if len(graph_df.index[0].split(':')) == 3:
		graph_df['Batch'] = graph_df.index.map(lambda x:x.split('_')[0])
	# graph_df['pert_id'] = graph_df.index.map(lambda x:x.split(':')[1])

	graph_df.rename(
		index=str, 
		columns={
			'SCS_centered_by_batch': 'p-value', 'cell': 'Cell', 'pert_time': 'Time', 
			'drug_class': 'Drug class', 'pert_dose': 'Dose',
			'pert_desc': 'Perturbation'},
		inplace=True)

	return graph_df, meta_df



