'''
Additional ORMs for the DrugPage app. 
'''
from collections import OrderedDict
from substrate import db

class Drug(db.Model):

    __tablename__ = 'drug'
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


    def __init__(self, pert_id):
        self.pert_id = pert_id

    def __repr__(self):
        return '<Drug %r>' % self.pert_id

    def to_dict(self):
        '''Convert metadata to a dict.'''
        d = OrderedDict()
        d['pert_id'] = self.pert_id
        d['Name'] = self.pert_iname
        if self.alt_name != 'NULL':
            d['Synonyms'] = self.alt_name.replace('|', '; ')
        d['Collection'] = self.pert_collection
        if self.pert_summary != 'NULL':
            d['Summary'] = self.pert_summary
        d['Canonical SMILES'] = self.canonical_smiles
        d['InChI key'] = self.inchi_key
        d['InChI string'] = self.inchi_string
        d['Molecular formula'] = self.molecular_formula
        d['Molecular weight'] = self.molecular_wt
        return d

    def get_external_links(self):
        '''Get all the external links and text to display.'''
        d = OrderedDict()
        if self.pubchem_cid != 'NULL':
            d['PubChem'] = (self.pubchem_cid, 
                'https://pubchem.ncbi.nlm.nih.gov/compound/%s' % self.pubchem_cid)

        if self.pert_url != 'NULL':
            d['Wikipedia'] = (self.pert_url, self.pert_url)

        if self.LSM_id != 'NULL':
            d['LIFE'] = (self.LSM_id, 
                'http://life.ccs.miami.edu/life/summary?mode=SmallMolecule&source=LINCS&input=%s' % self.LSM_id)

        d['SEP-L1000'] = (self.pert_id, 
            'http://maayanlab.net/SEP-L1000/#drug/%s' % self.pert_id)
        return d

