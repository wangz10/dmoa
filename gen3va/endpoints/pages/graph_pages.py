import os
import json

from flask import abort, Blueprint, render_template, request, Response, send_from_directory

from gen3va.database import *
from gen3va.config import Config


graph_pages = Blueprint('graph_pages',
                       __name__,
                       url_prefix=Config.BASE_URL + '/graph')

@graph_pages.before_app_first_request
def get_globals():

    global meta_df, N_SIGS, graph_df, drug_synonyms, drug_meta_df
    global graphs
    graphs = load_graphs_meta()

    drug_meta_df = load_drug_meta_from_db()
    
    # cyjs_filename = os.environ['CYJS']
    # graph_df = load_graph(cyjs_filename, meta_df)
    graph_df, meta_df = load_graph_from_db('Signature_Graph_CD_center_LM_sig-only_16848nodes.gml.cyjs',
      drug_meta_df=drug_meta_df)
    print meta_df.shape
    N_SIGS = meta_df.shape[0]

    print graph_df.head()

    drug_synonyms = load_drug_synonyms_from_db(meta_df, graph_df)


    return

@graph_pages.route('/')
def index_page():
	# The default main page
	url = 'graph/full'
	sdvConfig = {
		'colorKey': 'Cell',
		'shapeKey': 'Time',
		'labelKey': ['Batch', 'Perturbation', 'Cell', 'Dose', 'Time', 'Phase', 'MOA'],
	}


	return render_template('pages/graph.html', 
		script='main',
		# ENTER_POINT=ENTER_POINT,
		result_id='hello',
		graphs=graphs,
		url=url,
		sdvConfig=json.dumps(sdvConfig),
		)


@graph_pages.route('/<string:graph_name>', methods=['GET'])
def load_graph_layout_coords(graph_name):
	if request.method == 'GET':
		if graph_name == 'full':
			print graph_df.shape
			return graph_df.reset_index().to_json(orient='records')
		else:
			graph_df_, meta_df_ = load_graph_from_db(graph_name, drug_meta_df)
			print graph_df_.head()
			return graph_df_.reset_index().to_json(orient='records')

# @graph_pages.route('/<path:filename>')
# def send_file(filename):
# 	'''Serve static files.
# 	'''
# 	print filename
# 	import os
# 	print os.getcwd()
# 	return send_from_directory(graph_pages.static_folder, filename)
