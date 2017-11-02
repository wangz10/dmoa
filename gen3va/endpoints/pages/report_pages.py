"""Renders report pages.
"""

from flask import Blueprint, jsonify, redirect, request, render_template, \
    url_for, abort, make_response
from flask.ext.login import login_required

from substrate import Report, Tag, GeneSignature
from gen3va.database import Drug, load_graphs_meta
from gen3va.config import Config
from gen3va import database, report_builder


report_pages = Blueprint('report_pages',
                         __name__,
                         url_prefix=Config.REPORT_URL)

@report_pages.before_app_first_request
def get_globals():
    global graphs 
    graphs = load_graphs_meta()
    return


# @report_pages.route('/<string:tag_name>', methods=['GET'])
# def view_reports_associated_with_tag(tag_name):
#     """Renders page that lists all reports associated with a tag.
#     """
#     tag = database.get(Tag, tag_name, 'name')
#     if not tag:
#         abort(404)
#     has_no_reports = False
#     if len(tag.reports) == 0:
#         has_no_reports = True
#     has_enough_signatures = True
#     if len(tag.gene_signatures) < 3:
#         has_enough_signatures = False
#     return render_template('pages/reports-for-tag.html', tag=tag,
#                            has_no_reports=has_no_reports,
#                            has_enough_signatures=has_enough_signatures)


@report_pages.route('/<string:tag_name>', methods=['GET'])
def view_approved_report(tag_name):
    """Renders approved report page.
    """
    tag = database.get(Tag, tag_name, 'name')
    drug = database.get(Drug, tag_name, 'pert_id')
    if not tag:
    #     abort(404)
        return render_template('pages/report-empty.html',
                                drug=drug,
                                graphs=graphs)
    else:
        report = tag.approved_report
        if not report.complete(Config.SUPPORTED_ENRICHR_LIBRARIES):
            print 'Report for %s is not complete, building...' % tag.name
            print len(report.heat_maps)
            print len(report.enrichr_heat_maps)
            report_builder.rebuild(tag, category='cell')
        return render_template('pages/report.html',
                               tag=tag,
                               drug=drug,
                               report=report,
                               graphs=graphs
                               )

@report_pages.route('/signature/<string:extraction_id>', methods=['GET'])
def view_gene_signature(extraction_id):
    """Modal for gene signature.
    """
    gene_signature = database.get(GeneSignature, extraction_id, 'extraction_id')
    return render_template('pages/gene-signature.html',
                            gene_signature=gene_signature,
                            graphs=graphs)

@report_pages.route('/signature/download/<string:extraction_id>/<string:direction>', methods=['GET'])
def download_gene_list(extraction_id, direction):
    """Generate txt file for gene lists in gene signatures.
    direction should be attr name in one of ('combined_genes', 'up_genes', 'down_genes')
    """
    gene_signature = database.get(GeneSignature, extraction_id, 'extraction_id')
    gene_list = map(lambda x: x.gene.name, getattr(gene_signature, direction))
    # Make a file on-the-fly
    gene_list = '\n'.join(gene_list)
    filename = '%s-%s.txt' % (extraction_id, direction)

    response = make_response(gene_list)
    response.headers["Content-Disposition"] = "attachment; filename=%s" % filename
    return response

@report_pages.route('/signature/enrichr/<string:extraction_id>/<string:direction>', methods=['GET'])
def enrichr_gene_list(extraction_id, direction):
    """Get Enrichr result for gene lists in gene signatures.
    """
    raise NotImplementedError


# Utility methods
# ----------------------------------------------------------------------------

def _get_extraction_ids(request):
    """Returns extraction IDs from JSON post.
    """
    return [gs['extractionId'] for gs in request.json['gene_signatures']]
