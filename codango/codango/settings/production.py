# Production specific settings
from .development import *

# Parse database configuration from $DATABASE_URL
import dj_database_url

DATABASES = {
  'default': dj_database_url.config()
}

# Enable Connection Pooling
DATABASES['default']['ENGINE'] = 'django_postgrespool'