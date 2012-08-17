#coding=UTF-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
import urllib
import urllib2
import json
import md5
import hashlib
from mylib.myutil import http_post_multipart, https_post_multipart, urllib2_get_read_json, urllib2_post_read_json
from mylib.myvar import *

def test(request):
    return HttpResponse('Hello, test renren')

def oauth_request(request):
    url_params = {
        'client_id':key_api_renren,
        'redirect_uri':url_redirect_renren,
        'response_type':'code',
        'scope':scope_oauth_renren,
        }
    url_param = urllib.urlencode(url_params)
    url = '%s?%s'%(url_oauth_request_renren, url_param)
    print url
    return HttpResponseRedirect(url)

def oauth_redirect(request):
    code = request.REQUEST.get('code', None)
    if code == None: # need to log
        return HttpResponse('code is not exist')
    url_params = {
        'grant_type':'authorization_code',
        'client_id':key_api_renren,
        'redirect_uri':url_redirect_renren,
        'client_secret':key_secret_renren,
        'code':code,
        }
    url_param = urllib.urlencode(url_params)
    url = '%s?%s'%(url_oauth_redirect_renren, url_param)
    j = urllib2_get_read_json(url)
    expires_in = j['expires_in']
    refresh_token = j['refresh_token']
    access_token = j['access_token']
    user_id = j['user']['id']
    user_name = j['user']['name']
    print user_name, user_id, access_token, refresh_token, expires_in
    #######
    ## get album
    l = get_album(user_id, access_token)
    ## upload photo
    caption = str('test, 忽略它')
    aid = 0
    pic_path = './weibo/a.png'
    pic_name = 'a.png'
    l = photo_upload(access_token, caption, aid, pic_path, pic_name)
    return HttpResponse(str(l))


def get_sig(values):
    sig_str = ''
    for k in sorted(values.keys()):
        sig_str = '%s%s=%s'%(sig_str, k, values[k])
    sig_str = sig_str+key_secret_renren
    #print sig_str
    sig = hashlib.md5(sig_str).hexdigest()
    print sig
    return sig


def photo_upload(access_token, caption, aid, pic_path, pic_name):
    url_params = {
        'method':'photos.upload',
        'v':'1.0',
        'access_token':str(access_token),
        'format':'JSON',
        'caption':str(caption),
        'aid':str(aid), # 0 means mobile album
        #'place_id':placeid, not used at moment
        }
    sig = get_sig(url_params)
    url_params['sig'] = sig
    try:
        pic = open(pic_path, 'rb').read()
    except Exception as e:
        print 'error'
        return HttpResponse(str(e))
    host = 'api.renren.com'
    selector = '/restserver.do'
    fields = url_params 
    fields = url_params
    files = [('upload', pic_path, pic)]
    resp = http_post_multipart(host, selector, fields, files)
    return resp.read()


def get_album(user_id, access_token):
    url_params = {
        'method':'photos.getAlbums',
        'v':'1.0',
        'uid':str(user_id),
        'access_token':str(access_token),
        'format':'JSON',
        }
    sig = get_sig(url_params)
    url_params['sig'] = sig
    url_param = urllib.urlencode(url_params)
    j = urllib2_post_read_json(url_api_renren, url_param)
    l = []
    for album in j:
        update_time = album['update_time']
        name = album['name']
        aid = album['aid']
        size = album['size']
        photo_lists = get_photo(aid, size, user_id, access_token)
        l.append(photo_lists)
    return l

def get_photo(aid, count, user_id, access_token):
    url_params = {
        'method':'photos.get',
        'v':'1.0',
        'uid':str(user_id),
        'access_token':str(access_token),
        'aid':str(aid),
        'format':'JSON',
        #'page':'100',
        'count':str(count),
        }
    sig = get_sig(url_params)
    url_params['sig'] = sig
    url_param = urllib.urlencode(url_params)
    j = urllib2_post_read_json(url_api_renren, url_param)
    print len(j), count
    return j
