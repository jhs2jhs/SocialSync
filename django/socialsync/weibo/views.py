# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
import urllib
import urllib2
import json
import md5
import hashlib

def test(request):
    return HttpResponse('Hello, test weibo')

api_key = '497821139'
secret_key = 'a1817fce5282c64052d3f462cd5709d9'

def oauth_request(request):
    url_base = 'https://api.weibo.com/oauth2/authorize'
    redirect_url = 'http://127.0.0.1:8080/weibo/oauth_redirect'
    #redirect_url = 'http://127.0.0.1'
    url_params = {
        'client_id':api_key,
        'response_type':'code',
        'redirect_uri':redirect_url,
        }
    url_param = urllib.urlencode(url_params)
    url = '%s?%s'%(url_base, url_param)
    print url
    return HttpResponseRedirect(url)

def oauth_redirect(request):
    code = request.REQUEST.get('code', None)
    url_base = 'https://api.weibo.com/oauth2/access_token'
    redirect_url = 'http://127.0.0.1:8080/weibo/oauth_redirect'
    url_params = {
        'client_id':api_key,
        'client_secret':secret_key,
        'grant_type':'authorization_code',
        'redirect_uri':redirect_url,
        'code':code,
        }
    url_param = urllib.urlencode(url_params)
    #url = '%s?%s'%(url_base, url_param)
    #print url
    #return HttpResponseRedirect(url)
    req = urllib2.Request(url_base, url_param)
    resp = urllib2.urlopen(req)
    resp = resp.read()
    #req = urllib2.urlopen(url)
    #resp = req.read()
    print resp
    j = json.loads(resp)
    access_token = j['access_token']
    remind_in = j['remind_in']
    expires_in = j['expires_in']
    uid = j['uid']
    print access_token, remind_in, expires_in
    #print request.REQUEST
    url_base = 'https://api.weibo.com/2/statuses/user_timeline.json'
    url_params = {
        'access_token':access_token,
        'uid':uid,
        'count':50,
        'feature':1,
        }
    url_param = urllib.urlencode(url_params)
    url = '%s?%s'%(url_base, url_param)
    req = urllib2.urlopen(url)
    resp = req.read()
    j = json.loads(resp)
    for js in j['statuses']:
        if js.has_key('created_at'):
            created_at = js['created_at']
        else:
            created_at = ''
        if js.has_key('text'):
            text = js['text']
        else:
            text = ''
        if js.has_key('original_pic'):
            photo_path = js['original_pic']
            print created_at, text
            print photo_path
        #print js
    #print j
        print len(js), '****'
    print len(j), '######'
    print len(j['statuses'])
    url_base = 'https://upload.api.weibo.com/2/statuses/upload.json'
    status = 'this is only a test'
    pic_path = './weibo/a.png'
    try:
        pic = open(pic_path, 'rb').read()
    except Exception as e:
        print 'error'
        return HttpResponse(str(e))
    lat = 50
    lng = 50
    url_params = {
        'access_token':str(access_token),
        'status': status,
        'lat': str(lat),
        'long': str(lng),
        }
    host = 'upload.api.weibo.com'
    selector = '/2/statuses/upload.json'
    fields = url_params
    files = [('pic', 'a.png', pic)]
    print access_token
    print status
    resp = https_post_multipart(host, selector, fields, files)
    print resp
    return HttpResponse(resp.read())
    '''
    openner = urllib2.build_openner(MultipartPostHandler.MultipartPostHandler)
    urllib2.install_openner(openner)
    req = urllib2.Request(url_base, url_params)
    resp = 'hello'
    try:
        resp = urllib2.urlopen(req)
        resp = resp.read()
        print resp
    except urllib2.URLError, e:
        print 'url error'
    return HttpResponse(resp)
    '''
    

'''
    url_params = {
        'client_id':api_key,
        'client_secret':secret_key,
        'grant_type':'authorization_code',
        'redirect_uri':redierct_url,
        'code':code,
        }
'''


import httplib, mimetypes

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
    #return resp.status, res.reason, res.read()
    '''
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, errmsg, headers = h.getreply()
    return h.file.read()
    '''

def encode_multipart_formdata(fields, files=[]):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    import mimetools
    import mimetypes
    #BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
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
    #print L
    import sys
    print sys.getdefaultencoding()
    body = CRLF.join(L)
    print body
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
