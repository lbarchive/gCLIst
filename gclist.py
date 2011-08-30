#!/usr/bin/env python
'''Simple program for uploading files to Gist of GitHub.
'''


import sys


def errexit(errmsg):

  print >>sys.stderr, errmsg
  sys.exit(1)


try:
  import argparse
except ImportError:
  errexit('Please install argparse module: easy_install argparse')
import base64
import ConfigParser as cfgparse
try:
  import json
except ImportError:
  import simplejson as json
import os
import urllib
import urllib2


__program__ = 'gclist'
__author__ = 'Yu-Jie Lin'
__copyright__ = 'Copyright 2011'
__credits__ = ['Yu-Jie Lin']
__license__ = 'MIT'
__version__ = '0.1'
__maintainer__ = 'Yu-Jie Lin'
__email__ = 'livibetter@gmail.com'
__status__ = 'Development'


class GistClient(object):
  
  API_BASE = 'https://api.github.com'
  API_GIST_CREATE = '/gists'

  def __init__(self, username, password):
    
    self.username = username
    self.password = password

  def _fetch(self, url, data=None):
    
    headers = {}
    if self.username and self.password:
      headers['Authorization'] = 'Basic ' + base64.b64encode(
          '%s:%s' % (self.username, self.password))
    headers['Content-Type'] = 'application/json'

    req = urllib2.Request(url, headers=headers)
    if data:
      req.add_data(data)
    try:
      f = urllib2.urlopen(req)
      return f.read()
    except urllib2.HTTPError, e:
      if e.code == 201:
        # In Python 2.5, 201 Created counts as a HTTP Error
        return e.fp.read()
      print >>sys.stderr
      print >>sys.stderr, 'HTTP Error %d' % e.code
      print >>sys.stderr, e.fp.read()
      sys.exit(1)

  def _post(self, url, jobj):

    data = json.dumps(jobj, separators=(',', ':'))
    ret = self._fetch(url, data)
    return json.loads(ret)

  def upload(self, files, description=None, public=True):
    '''Upload files to a new gist or edit a gist with files.
    
    files is a list of file objects.
    '''
    json_files = {}
    for f in files:
      content = f.read()
      f.close()
      filename = os.path.basename(f.name)
      if f.name == '<stdin>':
        print 'Content from stdin.'
        sys.__stdin__.close()
        sys.__stdin__ = sys.stdin = open('/dev/tty')
        filename = raw_input('Please enter a filename: ')
      json_files[filename] = {'content': content}

    jobj = {'public': public, 'files': json_files}
    if description:
      jobj['description'] = description
    
    print 'Uploading...',
    sys.stdout.flush()
    jret = self._post(self.API_BASE + self.API_GIST_CREATE, jobj)
    print 'done'
    print

    print 'Gist %s was created at' % jret['id']
    print ' ', jret['html_url']
    print ' ', jret['git_pull_url']
    print
    if jret['user']:
      print 'User       :', jret['user']['login']
    else:
      print 'User       : Anonymous'
    print 'Public     : %s' % jret['public']
    print 'Description: %s' % jret['description']
    print
    print 'Files:'
    print '    <script src="https://gist.github.com/%s.js"> </script>' % jret['id']
    for fname in jret['files']:
      print
      print '  %s' % fname
      print '    %s' % jret['files'][fname]['raw_url']
      print '    <script src="https://gist.github.com/%s?%s"></script>' % (
          jret['id'],
          urllib.urlencode({'file': fname}),
          )
      

def get_username_password(cfg_paths, section):
  '''Returns username and password from config

  Returns (username, passwor) or (None, None) if not found
  '''
  cfg = cfgparse.ConfigParser()
  if cfg.read(cfg_paths):
    if section not in cfg.sections():
      errexit('You does not have "%s" config section' % section)
    kv = dict(cfg.items(section))
    if 'username' not in kv or 'password' not in kv or \
        not kv['username'] or not kv['password']:
      errexit('Your username or password is not configuared correctly.')
    return kv['username'], kv['password']
  return None, None


def main():
  
  parser = argparse.ArgumentParser(description='Simple program '
                                   'for uploading files to Gist of GitHub.')
  parser.add_argument('-a', '--anonymous', dest='anonymous',
                      default=False, action='store_true',
                      help='Upload anonymously (default: %(default)s)')
  parser.add_argument('-d', '--description', dest='description',
                      help='Description for Gist (default: %(default)s)')
  parser.add_argument('-p', '--private', dest='private',
                      default=False, action='store_true',
                      help='Set Gist to private (default: %(default)s)')
  parser.add_argument('-c', '--config', dest='section',
                      default='default',
                      help='Which INI section to use (default: %(default)s)')
  parser.add_argument(metavar='FILE', type=argparse.FileType('r'),
                      dest='files', nargs='*',
                      help='File to upload (default: %(default)s)')
  args = parser.parse_args()

  cfg_paths = (
      __program__ + 'rc',
      '%s/%s/config' % (
          os.environ.get('XDG_CONFIG_DIR', os.path.expanduser('~/.config')),
          __program__,
          ),
      )

  if args.anonymous:
    username, password = None, None
  else:
    username, password = get_username_password(cfg_paths, args.section)

  if not args.files:
    if sys.stdin.isatty():
      print 'Please supply at least a file.'
      sys.exit(0)
    args.files = [sys.stdin]

  client = GistClient(username, password)

  client.upload(files=args.files, description=args.description, public=not args.private)


if __name__ == "__main__":
  main()
