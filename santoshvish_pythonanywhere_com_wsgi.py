import os
import sys

path = os.path.expanduser('~/proj_mgmt')
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'proj_mgmt.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
