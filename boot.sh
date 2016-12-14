#!/usr/bin/env bash

adduser --disabled-password --gecos '' r
cd /dmoa/
mod_wsgi-express setup-server wsgi.py --port=80 --user r --group r --server-root=/etc/dmoa --socket-timeout=600 --limit-request-body=524288000
chmod a+x /etc/dmoa/handler.wsgi
chown -R r /dmoa/gen3va/static/
/etc/dmoa/apachectl start
tail -f /etc/dmoa/error_log