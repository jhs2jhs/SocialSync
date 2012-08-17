import httplib, mimetypes, mimetools
import urllib, urllib2
import json

######################
def http_post_multipart(host, selector, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTPConnection(host)
    headers = {
        'Content-type':content_type,
        'Content-length':str(len(body)),
        }
    h.request('POST', selector, body, headers)
    resp = h.getresponse()
    return resp

def https_post_multipart(host, selector, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTPSConnection(host)
    headers = {
        'Content-type':content_type,
        'Content-length':str(len(body)),
        }
    h.request('POST', selector, body, headers)
    resp = h.getresponse()
    return resp

def encode_multipart_formdata(fields, files=[]):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = mimetools.choose_boundary()
    CRLF = '\r\n'
    L = []
    for (key, value) in fields.items():
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
##########################

##########################
def urllib2_post_read_json(url_base, url_param):
    try:
        req = urllib2.Request(url_base, url_param)
        resp = urllib2.urlopen(req)
        resp = resp.read()
        j = json.loads(resp)
    except urllib2.URLError, e: # do some log
        j = {}
    except urllib2.HTTPError, e: # do some log
        j = {}
    except Exception, e: # do some log
        j = {}
    return j

def urllib2_get_read_json(url):
    try:
        req = urllib2.urlopen(url)
        resp = req.read()
        j = json.loads(resp)
    except urllib2.URLError, e:
        j = {}
    except urllib2.HTTPError, e:
        j = {}
    except Exception, e: 
        j = {}
    return j
    
