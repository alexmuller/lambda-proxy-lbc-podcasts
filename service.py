# -*- coding: utf-8 -*-

from os import getenv

import boto3
import urllib.parse
import urllib.request

def handler(event, context):
    url = 'http://lbc.audioagain.com'
    values = {
        'user_name': getenv('USERNAME'),
        'password': getenv('PASSWORD'),
    }

    data = urllib.parse.urlencode(values).encode('ascii')

    req = urllib.request.Request(url + '/', data)

    with urllib.request.urlopen(req) as response:
        session_id = response.getheader('Set-Cookie').split(';')[0].split('=')[1]

    xml_request = urllib.request.Request(url + '/podcast_feed.php?channel=subjames')
    xml_request.add_header('Cookie', 'PHPSESSID={0}'.format(session_id))

    xml_response = urllib.request.urlopen(xml_request)

    temporary_file = '/tmp/podcast.xml'
    bucket_name = getenv('S3_BUCKET_NAME')
    key = 'james-obrien--{0}.xml'.format(getenv('S3_FEED_KEY'))

    file = open(temporary_file, 'wb')
    file.write(xml_response.read())
    file.close()

    s3 = boto3.client('s3')
    s3.upload_file(temporary_file, bucket_name, key)
    s3.put_object_acl(ACL='public-read', Bucket=bucket_name, Key=key)

    return 'LBC podcasts updated successfully'
