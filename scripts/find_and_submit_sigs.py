import os
import json

import numpy as np
import pandas as pd
import requests
from pymongo import MongoClient
import matplotlib.pyplot as plt

conn = MongoClient('mongodb://146.203.54.131:27017/')

## 0. Get the genes first
coll = conn['LINCS_L1000_genes']['genes']
genes = coll.find_one({'tag': 'GSE70138'})['geneSymbol']
genes = np.array(genes)
print len(genes), genes[:10]

# the coll for signatures
coll = conn['L1000CDS2']['cpcd-gse70138']
# coll.find({''}, projection={'_id':False})

## 1. GROUP BY `pert_id` COUNT 
# cur = coll.aggregate([{
# 		'$group': {
# 			'_id': '$pert_id',
# 			'count': {'$sum': 1}
# 		}
# 	}])

# cur = coll.find({}, {'pert_id':True, 'pvalue':True, 'pert_id':True, 'sig_id':True})
# docs = [doc for doc in cur]
# meta_df = pd.DataFrame.from_records(docs).set_index('sig_id')
# print meta_df.shape
# meta_df.to_csv('meta_df.csv')

# count_df = pd.DataFrame.from_records([doc for doc in cur]).set_index('_id')
# count_df.to_csv('pert_id_sig_counts.csv')

# count_df['count'].plot(kind='hist', bins=25)
# plt.show()

meta_df = pd.read_csv('meta_df.csv').set_index('sig_id')
pert_ids = meta_df['pert_id'].unique()
print meta_df.head()
grouped_sorted = meta_df.groupby('pert_id')['pvalue'].apply(lambda x: x.order(ascending=True).head(50))
print grouped_sorted[:50]

# filter out pert_id with less than 20 signatures
pert_id_counts = meta_df.reset_index().groupby('pert_id')['sig_id'].count()
print pert_id_counts[:10]

pert_ids_kept = pert_id_counts[pert_id_counts > 20].index.tolist()
print 'Number of pert_id to keep: %d' % len(pert_ids_kept)
print grouped_sorted.shape
grouped_sorted = grouped_sorted[pert_ids_kept].reset_index()
print grouped_sorted.shape
n_sigs = grouped_sorted.shape[0]
print 'Number of sig_id to insert: %d' % n_sigs
print grouped_sorted[:50]
print grouped_sorted[:50].loc[1, 'sig_id']

# count_df = pd.read_csv('pert_id_sig_counts.csv').set_index('_id')
# print count_df.head()
# print count_df.shape
# counts = count_df['count']
# m = counts >= 20
# print 'Number of pert_id kept:', m.sum()

# pert_ids_kept = count_df.loc[m].index.tolist()
# projection = {'_id':False, 'chdirLm':False, 'upGenes':False, 'dnGenes':False}

# cur = coll.find({'pert_id': {'$in': pert_ids_kept}}, 
# 	projection=projection)

essential_keys = set(['sigIdx', 'chdirFull', 'pert_id', 'cell_id', 'pert_desc', 'pert_dose', 'pert_time', 'sig_id'])

for i in range(n_sigs):
	sig_id = grouped_sorted.loc[i, 'sig_id']
	doc = coll.find_one({'sig_id': sig_id}, {'_id':False})

	if len(set(doc) & essential_keys) == len(essential_keys):
		# make sure all those keys exist
		# if doc['sigIdx'] > 1:
		if type(doc['sigIdx']) == list:
			sigIdx = np.array(doc['sigIdx']).astype(int) - 1
			if type(sigIdx) == np.ndarray:
				if len(sigIdx) > 20:

					sig_genes = genes[sigIdx]

					cd_coefs = np.array(doc['chdirFull'])[sigIdx]
					ranked_genes = pd.DataFrame({'gene': sig_genes, 'val': cd_coefs})
					# drop -666
					ranked_genes = ranked_genes.loc[~np.in1d(ranked_genes['gene'], ['-666'])]
					# get the largest abs for same genes
					ranked_genes = ranked_genes.groupby('gene').agg({'val': lambda x: max(max(x), min(x), key=abs)})

					ranked_genes = zip(ranked_genes.index, ranked_genes.val)

					# print ranked_genes[:5]

					payload = {
						'ranked_genes': ranked_genes,
						'diffexp_method': 'chdir',
						'tags': [doc['pert_id']],
						'gene': None,
						'cell': doc['cell_id'],
						'perturbation': doc['pert_desc'],
						'disease': None,
						## optional metadata
						'metadata[pert_id]': doc['pert_id'],
						'metadata[dose]': doc['pert_dose'],
						'metadata[time]': doc['pert_time'],
						'metadata[sig_id]': doc['sig_id'],
					}
					# print doc['sig_id']
					
					resp = requests.post('http://127.0.0.1:8083/g2e/api/extract/upload_gene_list', 
						data=json.dumps(payload))

	if i % 100 == 0:
		print i, n_sigs
