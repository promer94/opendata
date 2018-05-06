import datetime
import os

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'AKIAI5UYGY54BQI3ZF5Q')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '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')
AWS_FILE_EXPIRE = 200
AWS_QUERYSTRING_AUTH = True


STATICFILES_STORAGE = 'fitsecret.settings.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'aws-website-datavisualazation-azh49')
S3DIRECT_REGION = 'us-west-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL + 'static/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}