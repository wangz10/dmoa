'''
Additional ORMs for the DrugPage app. 
'''
import json
import httplib
from urlparse import urlparse
from collections import OrderedDict
from substrate import db

from gen3va.database.utils import session_scope


def get_status_code(url):
    ## modified from: https://stackoverflow.com/questions/1140661/what-s-the-best-way-to-get-an-http-response-code-from-a-url
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        None instead.
    """
    try:
        o = urlparse(url)
        conn = httplib.HTTPConnection(o.hostname)
        conn.request("HEAD", o.path)
        return conn.getresponse().status
    except StandardError:
        return None


def isnull(value):
    if value != 'NULL' and value is not None:
        return False
    else:
        return True


class Drug(db.Model):

    __tablename__ = 'drug_repurposedb'
    pert_id = db.Column(db.String(32), primary_key=True)
    alt_name = db.Column(db.String(255))
    pert_iname = db.Column(db.String(255), nullable=False)
    LSM_id = db.Column(db.String(16))
    mls_id = db.Column(db.String(16))
    ncgc_id = db.Column(db.String(16))
    pert_collection = db.Column(db.String(16))
    pert_icollection = db.Column(db.String(16))
    pert_summary = db.Column(db.Text)
    pert_url = db.Column(db.Text)
    pubchem_cid = db.Column(db.String(16))
    canonical_smiles = db.Column(db.Text)
    inchi_key = db.Column(db.Text)
    inchi_string = db.Column(db.Text)
    molecular_formula = db.Column(db.Text)
    molecular_wt = db.Column(db.Float)
    structure_url = db.Column(db.Text)
    moa = db.Column(db.Text)
    target = db.Column(db.Text)
    phase = db.Column(db.Text)
    ingredient_id = db.Column(db.Integer)



    def __init__(self, pert_id):
        self.pert_id = pert_id

    def __repr__(self):
        return '<Drug %r>' % self.pert_id

    def to_dict(self):
        '''Convert metadata to a dict.'''
        d = OrderedDict()
        d['pert_id'] = self.pert_id
        d['Name'] = self.pert_iname
        if not isnull(self.alt_name):
            d['Synonyms'] = self.alt_name.replace('|', '; ')
        d['Collection'] = self.pert_collection
        if not isnull(self.pert_summary):
            d['Summary'] = self.pert_summary
        if isnull(self.moa):
            d['MOA'] = 'Unknown'
        d['MOA'] = self.moa
        if isnull(self.target):
            d['Target(s)'] = 'Unknown'
        d['Target(s)'] = self.target
        if isnull(self.phase):
            d['Phase'] = 'Unknown'
        d['Phase'] = self.phase
        d['Canonical SMILES'] = self.canonical_smiles
        d['InChI key'] = self.inchi_key
        d['InChI string'] = self.inchi_string
        d['Molecular formula'] = self.molecular_formula
        d['Molecular weight'] = self.molecular_wt
        return d

    def get_external_links(self):
        '''Get all the external links and text to display.'''
        d = OrderedDict()
        if not isnull(self.pubchem_cid):
            d['PubChem'] = (self.pubchem_cid, 
                'https://pubchem.ncbi.nlm.nih.gov/compound/%s' % self.pubchem_cid)

        if not isnull(self.pert_url):
            pert_url = self.pert_url.split(',')[0]
            d['Wikipedia'] = (pert_url, pert_url)

        if not isnull(self.LSM_id):
            d['LINCS Data Portal'] = (self.LSM_id, 
                'http://lincsportal.ccs.miami.edu/SmallMolecules/#/view/%s' % self.LSM_id)
            d['iLINCS'] = (self.LSM_id, 
                'http://www.ilincs.org/ilincs/perturbagen/compound/%s' % self.LSM_id)

        d['SEP-L1000'] = (self.pert_id, 
            'http://maayanlab.net/SEP-L1000/#drug/%s' % self.pert_id)
        return d

    def get_structure_url(self):
        if not isnull(self.LSM_id):
            url = 'http://life.ccs.miami.edu/life/web/images/sm-images/400/%s.png' % self.LSM_id
        else:
            url = 'http://maayanlab.net/SEP-L1000/img/cpd-images/%s.png' % self.pert_id

        # Test if the image exists
        resp_code = get_status_code(url)
        if resp_code != 200:
            url = 'https://s3.amazonaws.com/data.clue.io/trimmed_perts/%s.png' % self.pert_id
        return url

    def has_clinical_info(self):
        return not isnull(self.ingredient_id)

    def get_rx_counts(self, nrows=20):
        with session_scope() as session:
            query_results = session\
                .execute("""SELECT co_rx.jaccard_index AS x, 
                    rx_counts.count AS y,
                    co_rx.count AS z, rx_counts.ingredient AS name
                    FROM co_rx
                    LEFT JOIN rx_counts ON rx_counts.`id`=co_rx.`co_prescribed_drug_id`
                    WHERE ingredient_id=:ingredient_id
                    ORDER BY x DESC
                    LIMIT :nrows;
                    """, params={'ingredient_id': self.ingredient_id, 'nrows':nrows})

            if query_results.rowcount == 0:
                return None
            else:
                field_names = query_results.keys()
                rx_counts = query_results.fetchall()
                rx_counts = [dict(zip(field_names, row)) for row in rx_counts]
                results = {'data': rx_counts, 'name': 'co_prescribed_drug'}
                return json.dumps(results)

    def get_dx_counts(self, nrows=20):
        with session_scope() as session:
            query_results = session\
                .execute("""SELECT co_dx.jaccard_index AS x, 
                    dx_counts.count AS y, 
                    co_dx.count AS z, dx_counts.ICD9, 
                    dx_counts.diagnosis AS name
                    FROM co_dx
                    LEFT JOIN dx_counts ON dx_counts.`id`=co_dx.`diagnosis_id`
                    WHERE ingredient_id=:ingredient_id
                    ORDER BY x DESC
                    LIMIT :nrows
                    """, params={'ingredient_id': self.ingredient_id, 'nrows':nrows})

            if query_results.rowcount == 0:
                return None
            else:
                field_names = query_results.keys()
                dx_counts = query_results.fetchall()
                dx_counts = [dict(zip(field_names, row)) for row in dx_counts]
                results = {'data': dx_counts, 'name': 'diagnoses'}
                return json.dumps(results)



    def get_rx_age_kde(self):
        '''Get the KDE smoothened age distribution for the prescription of this drug.
        '''
        with session_scope() as session:
            query_results = session\
                .execute("""SELECT age_years, density 
                    FROM rx_age_kde
                    WHERE ingredient_id=:ingredient_id
                    """, params={'ingredient_id': self.ingredient_id})
            if query_results.rowcount == 0:
                return None
            else:
                results = query_results.fetchall()
                age_years = [item[0] for item in results]
                density = [item[1] for item in results]
                results = {'density': density, 'age_years':age_years, 'name': self.pert_iname}
                return json.dumps(results)

