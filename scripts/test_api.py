import json
import requests

payload = {
    'ranked_genes': [
        [
            'CPSF3',
            0.000631847
        ],
        [
            'CLEC18B',
            0.00876892
        ],
        [
            'RTDR1',
            0.0000692485
        ],
        [
            'MYLPF',
            0.00218427
        ],
        [
            'KIF2B',
            0.0000457653
        ],
        [
            'SMPDL3A',
            0.00876879
        ],
        [
            'FAM171A2',
            0.00442025
        ],
        [
            'RASGRF2',
            0.0145588
        ],
        [
            'ROCK2',
            0.00218436
        ]
    ],
    'diffexp_method': 'chdir',
    'tags': ['test_tag', 'drug1'],
    'gene': 'STAT3',
    'cell': None,
    'perturbation': None,
    'disease': None,
    'metadata[drug]': 'drug1'
}

# url = 'http://amp.pharm.mssm.edu/gen3va/api/1.0/upload'
# url = 'http://127.0.0.1:8084/gen3va/api/1.0/upload/upload2'
## Instead of POST to gen3va, directly POST to g2e endpoint: 
url = 'http://127.0.0.1:8083/g2e/api/extract/upload_gene_list'
resp = requests.post(url, data=json.dumps(payload))
print resp.status_code


