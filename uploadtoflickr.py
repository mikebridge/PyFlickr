#!/usr/bin/env python
import datetime

import os
import getopt
import re
import sys
# flickrapi does not work with python 3
import flickrapi
import webbrowser

__author__ = 'Mike Bridge'

api_key = u'7b546b3c5860caa10ddd41448eeaf7e7'
api_secret = u'83c8e48221459d91'

flickr = flickrapi.FlickrAPI(api_key, api_secret)

print('authenticating...')

# Only do this if we don't have a valid token already
if not flickr.token_valid(perms=u'delete'):

    # Get a request token
    flickr.get_request_token(oauth_callback='oob')

    # Open a browser at the authentication URL. Do this however
    # you want, as long as the user visits that URL.
    authorize_url = flickr.auth_url(perms=u'delete')
    webbrowser.open_new_tab(authorize_url)

    # Get the verifier code from the user. Do this however you
    # want, as long as the user gives the application the code.
    #verifier = unicode(raw_input('Verifier code: '))
    print(authorize_url);
    verifier = raw_input("Enter the authorization code: ");
    uverifier = unicode(verifier, "utf-8")
    print("verifier is "+uverifier)
    # Trade the request token for an access token
    flickr.get_access_token(uverifier)

print('uploading...')

class FileWithCallback(object):
    def __init__(self, filename, callback):
        self.file = open(filename, 'rb')
        self.callback = callback
        # the following attributes and methods are required
        self.len = os.path.getsize(filename)
        self.fileno = self.file.fileno
        self.tell = self.file.tell

    def read(self, size):
        if self.callback:
            self.callback(self.tell() * 100 // self.len)
        return self.file.read(size)

def callback(progress):
    print(".")


def upload(filename):
    print("uploading ",filename)
    params = dict()
    params['fileobj'] = FileWithCallback(filename, callback)
    rsp = flickr.upload(params)
    #print(rsp)

def get_title(filename):
    print("matching "+filename)
    d = re.match(r"isaacsharbour-(\d\d\d\d)-(\d\d)-(\d\d)-(\d\d)(\d\d).jpg", filename)
    if not(d):
        print("Failed: " + d.string)
        sys.exit(1)
    year = int(d.group(1))
    month = int(d.group(2).lstrip("0"))
    day = int(d.group(3).lstrip("0"))
    hour = int(d.group(4).lstrip("0"))
    minute = int(d.group(5).lstrip("0"))
    photodate = datetime.datetime(year, month, day, hour, minute)
    print(photodate)
    dayformat = '{d:%B} {d.day} {d.year}'.format(d=photodate)
    timeformat = '{d:%I}:{d.minute:02} {d:%p}'.format(d=photodate).lstrip("0")
    return unicode("Isaac's Harbour, " + dayformat + ", " + timeformat, "utf-8")


def main(argv):
    print('ARGV      :', sys.argv[1:])
    verbose=False
    files=[]
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hf:v', ['files=',
                                                             'verbose',
                                                             'version=',
                                                             ])
    for opt, arg in options:
        if opt == '-h':
            print('uploadtoflickr.py <file> [<file> ...]')
            sys.exit()
        elif opt in ('-v', '--verbose'):
            verbose = True
        #elif opt in ("-", "--files"):
        #    inputfile = arg
        #elif opt in ("-o", "--ofile"):
        #    outputfile = arg
    #print('VERSION   :', version)
    #print 'VERBOSE   :', verbose
    #print 'OUTPUT    :', output_filename
    print('REMAINING :', remainder)
    files=remainder

    for file in files:
            try:
                print("UPLOADING ", file)
                print(get_title(file))
                #flickr.upload(
                #    filename=file.encode('utf-8'),
                #    title= get_title(file),
                #    is_public=1
                #    #os.path.splitext(os.path.basename(file_['path']))[0],
                #    #is_public=self.photo_settings.get('is_public', 0),
                #    #is_friend=self.photo_settings.get('is_friend', 0),
                #    #is_family=self.photo_settings.get('is_family', 0),
                #    #tags=self.path_to_tags(file_['path'].replace(self.path, ''))
                #)
                print("DONE")
                #print '{} uploaded'.format(file_['path'])
            except:
                print('{} failed upload'.format(file))

if __name__ == "__main__":
   main(sys.argv[1:])

