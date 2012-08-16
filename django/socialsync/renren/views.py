# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
import urllib
import urllib2
import json
import md5
import hashlib

def test(request):
    return HttpResponse('Hello, test renren')

api_key = 'a2dcb2e64a2d484192b5288bd9dd1c3a'
secret_key = 'c047cd6c402e45888780cf0631b86b21'
api_url = 'http://api.renren.com/restserver.do'

def oauth_request(request):
    url_base = 'https://graph.renren.com/oauth/authorize'
    redirect_url = 'http://localhost:8080/renren/oauth_redirect'
    scope = 'create_album read_user_photo photo_upload read_user_album'
    #scope = 'read_user_photo'
    #scope = 'read_user_album'
    url_params = {
        'client_id':api_key,
        'redirect_uri':redirect_url,
        'response_type':'code',
        'scope':scope,
        }
    url_param = urllib.urlencode(url_params)
    url = '%s?%s'%(url_base, url_param)
    print url
    return HttpResponseRedirect(url)

#def oauth_redirect(request):
    

def oauth_redirect(request):
    code = request.REQUEST.get('code', None)
    if code == None:
        print request.REQUEST
        return HttpResponse('cool')
    print code
    url_base = 'https://graph.renren.com/oauth/token'
    #response_url = 'http://localhost:8080/renren/oauth_response'
    redirect_url = 'http://localhost:8080/renren/oauth_redirect'
    url_params = {
        'grant_type':'authorization_code',
        'client_id':api_key,
        'redirect_uri':redirect_url,
        'client_secret':secret_key,
        'code':code,
        }
    url_param = urllib.urlencode(url_params)
    url = '%s?%s'%(url_base, url_param)
    print url
    req = urllib2.urlopen(url)
    resp = req.read()
    print resp
    j = json.loads(resp)
    expires_in = j['expires_in']
    refresh_token = j['refresh_token']
    access_token = j['access_token']
    user_id = j['user']['id']
    user_name = j['user']['name']
    print user_name, user_id, access_token, refresh_token, expires_in
    #return HttpResponseRedirect(url)
    ## get album
    l = get_album(user_id, access_token)
    return HttpResponse(str(l))


def get_album(user_id, access_token):
    url_base = api_url
    values = {
        'method':'photos.getAlbums',
        'v':'1.0',
        'uid':user_id,
        'access_token':access_token,
        'format':'JSON',
        }
    sig_str = ''
    for k in sorted(values.keys()):
        sig_str = '%s%s=%s'%(sig_str, k, values[k])
    sig_str = sig_str+secret_key
    print sig_str
    sig = hashlib.md5(sig_str).hexdigest()
    print sig
    values['sig'] = sig
    print values, '==========****'
    data = urllib.urlencode(values)
    print data, "=========="
    req = urllib2.Request(url_base, data)
    resp = urllib2.urlopen(req)
    resp = resp.read()
    print resp
    j = json.loads(resp)
    l = []
    for album in j:
        update_time = album['update_time']
        name = album['name']
        aid = album['aid']
        size = album['size']
        print size
        photo_lists = get_photo(aid, size, user_id, access_token)
        #l[aid] = photo_lists
        l.append(photo_lists)
        #l = photo_lists
    #print l
    return l

def get_photo(aid, count, user_id, access_token):
    url_base = api_url
    values = {
        'method':'photos.get',
        'v':'1.0',
        'uid':user_id,
        'access_token':access_token,
        'aid':aid,
        'format':'JSON',
        #'page':'100',
        'count':count,
        }
    sig_str = ''
    for k in sorted(values.keys()):
        sig_str = '%s%s=%s'%(sig_str, k, values[k])
    sig_str = sig_str+secret_key
    sig = hashlib.md5(sig_str).hexdigest()
    values['sig'] = sig
    data = urllib.urlencode(values)
    req = urllib2.Request(url_base, data)
    resp = urllib2.urlopen(req)
    resp = resp.read()
    j = json.loads(resp)
    print len(j), count
    return resp
