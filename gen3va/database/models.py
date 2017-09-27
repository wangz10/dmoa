'''
Additional ORMs for the DrugPage app. 
'''
import json
from collections import OrderedDict
from substrate import db

from gen3va.database.utils import session_scope


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
                ' http://lincsportal.ccs.miami.edu/SmallMolecules/#/view/%s' % self.LSM_id)

        d['SEP-L1000'] = (self.pert_id, 
            'http://maayanlab.net/SEP-L1000/#drug/%s' % self.pert_id)
        return d

    def get_structure_url(self):
        if not isnull(self.LSM_id):
            url = 'http://life.ccs.miami.edu/life/web/images/sm-images/400/%s.png' % self.LSM_id
        else:
            url = 'http://maayanlab.net/SEP-L1000/img/cpd-images/%s.png' % self.pert_id
        return url

    def get_rx_counts(self, limit=20):
        with session_scope() as session:
            rx_counts = session\
                .execute("""SELECT `co_prescribed_drug`, `count` 
                    FROM `co_rx` 
                    WHERE `pert_id`='%s' 
                    ORDER BY count DESC
                    LIMIT %s
                    """ % (self.pert_id, limit))\
                .fetchall()

            if len(rx_counts) == 0:
                return None
            else:
                drugs = [ item[0] for item in rx_counts ]
                counts = [ item[1] for item in rx_counts ]
                results = {'categories': drugs, 'counts': counts, 'name': 'co_prescribed_drug'}
                return json.dumps(results)

    def get_dx_counts(self, limit=20):
        with session_scope() as session:
            dx_counts = session\
                .execute("""SELECT `diagnosis`, `count` 
                    FROM `co_dx` 
                    WHERE `pert_id`='%s' 
                    ORDER BY count DESC
                    LIMIT %s
                    """ % (self.pert_id, limit))\
                .fetchall()

            if len(dx_counts) == 0:
                return None
            else:
                diagnoses = [ item[0] for item in dx_counts ]
                counts = [ item[1] for item in dx_counts ]
                results = {'categories': diagnoses, 'counts': counts, 'name': 'diagnoses'}
                return json.dumps(results)

