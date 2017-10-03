"""Interface for endpoints module.
"""

from api.download_api import download_api
from api.upload_api import upload_api
from api.signature_external_redirect_api import signature_external_redirect_api
from api.signature_api import signature_api

from pages.admin_pages import admin_pages
from pages.auth_pages import auth_pages
from pages.error_page import error_page
from pages.menu_pages import menu_pages
from pages.report_pages import report_pages
from pages.tag_pages import tag_pages
from pages.signature_pages import signature_pages