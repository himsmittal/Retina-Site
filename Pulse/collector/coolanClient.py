from urlBuilder import UrlBuilder
from cookielib import CookieJar
from base64 import b64encode
import urllib2


class CoolanClient(object):
    def __init__(self, host, http_scheme):
        self.host = host
        self.http_scheme = http_scheme
        self.cookie_jar = None

    def login(self, user, password):
        self._enable_cookies()
        url = UrlBuilder(self.host, '/v1/auth/login', {}, self.http_scheme)
        userAndPass = b64encode('%s:%s' % (user, password)).decode("ascii")
        request = urllib2.Request(url.get_url_with_query_params())
        request.get_method = lambda:'POST'
        request.add_header("Authorization", "Basic %s" % userAndPass)
        urllib2.urlopen(request)

    def _enable_cookies(self):
        jar = CookieJar()
        cookie_handler = urllib2.HTTPCookieProcessor(jar)
        cookie_opener = urllib2.build_opener(cookie_handler)
        urllib2.install_opener(cookie_opener)
        self.cookie_jar = jar
