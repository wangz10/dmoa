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

# count_df = pd.DataFrame.from_records([doc for doc in cur]).set_index('_id')
# count_df.to_csv('pert_id_sig_counts.csv')

# count_df['count'].plot(kind='hist', bins=25)
# plt.show()

count_df = pd.read_csv('pert_id_sig_counts.csv').set_index('_id')
print count_df.head()
print count_df.shape
counts = count_df['count']
m = counts >= 20
print 'Number of pert_id kept:', m.sum()

pert_ids_kept = count_df.loc[m].index.tolist()
projection = {'_id':False, 'chdirLm':False, 'upGenes':False, 'dnGenes':False}

# cur = coll.find({'pert_id': {'$in': pert_ids_kept}}, 
# 	projection=projection)



c = 0
## testing
# pert_ids_kept = ['BRD-K49055432']
# pert_ids_kept = ['BRD-K49468759']
## a small batch
# pert_ids_kept = pert_ids_kept[:5]
pert_ids_kept = pert_ids_kept[5:100]

for pert_id in pert_ids_kept:

	cur = coll.find({'pert_id': pert_id}, 
		projection={'_id':False, 'chdirLm':False, 
			'upGenes':False, 'dnGenes':False}).sort('pvalue', 1)
	print c, pert_id, cur.count()
	c += 1

	i = 0
	for doc in cur:
		i += 1
		if i > 50:
			break
		else:
			sigIdx = np.array(doc['sigIdx']).astype(int)
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
				'tags': ['LINCS-L1000-trt_cp', doc['pert_id'], doc['pert_desc'].lower()],
				'gene': None,
				'cell': doc['cell_id'],
				'perturbation': doc['pert_desc'],
				'disease': None,
				'title': doc['sig_id'],
			}
			# print doc['sig_id']
			
			resp = requests.post('http://amp.pharm.mssm.edu/gen3va/api/1.0/upload', 
				data=json.dumps(payload))
