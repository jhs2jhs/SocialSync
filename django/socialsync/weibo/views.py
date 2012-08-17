# coding=UTF-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
import urllib
import urllib2
import json
import md5
import hashlib
from mylib.myutil import https_post_multipart, urllib2_post_read_json, urllib2_get_read_json
from mylib.myvar import *

def test(request):
    return HttpResponse('Hello, test weibo')

def oauth_request(request):
    url_params = {
        'client_id':key_api_weibo,
        'response_type':'code',
        'redirect_uri':url_redirect_weibo,
        }
    url_param = urllib.urlencode(url_params)
    url = '%s?%s'%(url_oauth_request_weibo, url_param)
    return HttpResponseRedirect(url)

def oauth_redirect(request):
    code = request.REQUEST.get('code', None)
    if code == None: # need to log
        return HttpResponse('code is not exist')
    url_params = {
        'client_id':key_api_weibo,
        'client_secret':key_secret_weibo,
        'grant_type':'authorization_code',
        'redirect_uri':url_redirect_weibo,
        'code':str(code),
        }
    url_param = urllib.urlencode(url_params)
    j = urllib2_post_read_json(url_oauth_redirect_weibo, url_param)
    # user may reject the auth. 
    print j
    access_token = j['access_token']
    remind_in = j['remind_in']
    expires_in = j['expires_in']
    uid = j['uid']
    print access_token, remind_in, expires_in
    ## save it into database, also need to check refresh
    r = user_timeline(access_token, uid, 50, 1)
    #####
    status = str('this is only a test, 忽略他')
    pic_name = 'a.png'
    pic_path = './weibo/a.png'
    lat = 50
    lng = 50
    r = photo_upload(access_token, status, pic_name, pic_path, lat, lng)
    return HttpResponse(r)

def photo_upload(access_token, status, pic_name, pic_path, lat, lng):
    try:
        pic = open(pic_path, 'rb').read()
    except Exception as e:
        print 'error'
        return HttpResponse(str(e))
    url_params = {
        'access_token':str(access_token),
        'status': str(status),
        'lat': str(lat),
        'long': str(lng),
        }
    host = 'upload.api.weibo.com'
    selector = '/2/statuses/upload.json'
    fields = url_params
    files = [('pic', pic_path, pic)]
    resp = https_post_multipart(host, selector, fields, files)
    return resp.read()

# user_time(access_token, uid, 50, 1)
def user_timeline(access_token, uid, count, feature):
    url_params = {
        'access_token':access_token,
        'uid':uid,
        'count':count,
        'feature':1, # 1 means yuanchuang
        }
    url_param = urllib.urlencode(url_params)
    url = '%s?%s'%(url_user_timeline_weibo, url_param)
    j = urllib2_get_read_json(url)
    for js in j['statuses']:
        created_at = ''
        if js.has_key('created_at'):
            created_at = js['created_at']
        text = ''
        if js.has_key('text'):
            text = js['text']
        lat = ''
        lng = ''
        if js.has_key('geo'):
            geo = js['geo']
            if geo != None and geo.has_key('coordinates'):
                geo = geo['coordinates']
                if len(geo) == 2:
                    lat = geo[0]
                    lng = geo[1]
        if js.has_key('original_pic'):
            photo_path = js['original_pic']
            print lat, lng, created_at, text
            print photo_path
            ###### do some work here
        print len(js), '****'
    print len(j), '######'
    print len(j['statuses'])
    return j['statuses']


