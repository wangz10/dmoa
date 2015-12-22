"""Handles global configurations.
"""

import os


class Config(object):
    with open('gen3va/app.conf') as f:
        lines = [x for x in f.read().split('\n')]

    DEBUG = lines[1] == 'True'
    SERVER_FILE_ROOT = os.path.dirname(os.getcwd()) + '/gen3va/gen3va'

    BASE_URL = '/gen3va'
    BASE_API_URL = BASE_URL + '/api/1.0'
    BASE_PCA_URL = BASE_URL + '/pca'
    BASE_CLUSTER_URL = BASE_URL + '/cluster'

    REPORT_URL = BASE_URL + '/report'
    TAG_URL = BASE_URL + '/tag'
    METADATA_URL = BASE_URL + '/metadata'

    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_DATABASE_URI = lines[0]

    # Downstream applications
    if DEBUG:
        G2E_URL = 'http://localhost:8083/g2e'
        SERVER = 'http://localhost:8084/gen3va'
    else:
        G2E_URL = 'http://amp.pharm.mssm.edu/g2e'
        SERVER = 'http://amp.pharm.mssm.edu/gen3va'

    BASE_RESULTS_URL = G2E_URL + 'results'
    JSON_HEADERS = {'content-type': 'application/json'}
    CLUSTERGRAMMER_URL = 'http://amp.pharm.mssm.edu/clustergrammer'
    ENRICHR_URL = 'http://amp.pharm.mssm.edu/Enrichr'
    L1000CDS2_URL = 'http://amp.pharm.mssm.edu/L1000CDS2'
