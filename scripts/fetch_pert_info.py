"""Fetch additional info for missing pert_ids and insert into `drug` table.
"""

from pprint import pprint
import pandas as pd
from sqlalchemy import create_engine
import requests

engine = create_engine('mysql://root:@localhost/euclid')
existing_drugs = pd.read_sql('drug', engine)
# print existing_drugs.head()


def get_pert_info(pert_id):
	url = 'http://lincsportal.ccs.miami.edu/dcic/api/fetchmolecules?facet=source,assays,SM_Category,SM_Provider&limit=10&searchTerm=text:(%22+'+ pert_id + ' +%22)+&skip=0&sort=Score+desc'
	resp = requests.get(url)
	resp = resp.json()
	assert resp['results']['totalDocuments'] == 1
	resp = resp['results']['documents'][0]
	assert pert_id in resp['SM_Center_Compound_ID']

	# pprint(resp)
	alt_name = None
	if 'SM_Alternative_Name' in resp:
		alt_name = '|'.join(resp['SM_Alternative_Name'])
	obj = {
		'pert_id': pert_id,
		'alt_name': alt_name,
		'pert_iname': resp['SM_Name'],
		'LSM_id': resp['SM_LINCS_ID'],
		'mls_id': None,
		'ncgc_id': None,
		'pert_collection': None,
		'pert_icollection': None,
		'pert_summary': None,
		'pert_url': None,
		'pubchem_cid': resp.get('SM_PubChem_CID'),
		'canonical_smiles': resp.get('SM_SMILES_Parent'),
		'inchi_key': None,
		'inchi_string': resp.get('SM_InChi_Parent'),
		'molecular_formula': resp.get('MOLECULAR_FORMULA'),
		'molecular_wt': resp.get('SM_Molecular_Mass'),
		'structure_url': 'http://life.ccs.miami.edu/life/web/images/sm-images/400/%s.png' % resp['SM_LINCS_ID']

	}
	return obj
	

# http://lincsportal.ccs.miami.edu/dcic/api/fetchmolecules?facet=source,assays,SM_Category,SM_Provider&limit=10&searchTerm=text:(%22BRD-A18328003%22)+&skip=0&sort=Score+desc
# resp = get_pert_info('BRD-A18328003')
# resp = get_pert_info('BRD-K08109215')

tags = pd.read_sql('tag', engine)['name'].tolist()
missing_pert_ids = set(tags) - set(existing_drugs['pert_id'])

objs = []
for pert_id in missing_pert_ids:
	obj = get_pert_info(pert_id)
	objs.append(obj)

objs = pd.DataFrame.from_records(objs)

objs = objs[existing_drugs.columns]
print objs

objs.to_sql('drug', engine, if_exists='append', index=False)
