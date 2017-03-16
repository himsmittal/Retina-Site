from urlBuilder import UrlBuilder
from errorMessages import THREAD_ERROR_TEMPLATE
from threading import currentThread
from logMessages import *
import urllib2, json, sys

logger = logger(__name__)


class MetricTs(object):
    def __init__(self, host, scheme):
        self.host = host
        self.scheme = scheme
        self.params = {}
        self.path = None

    def get_machine_details(self, queue):
        while True:
            item = queue.get()
            self.params['machineEntityId'] = item[0]
            url = UrlBuilder(self.host, self.path, self.params, self.scheme)
            resp = urllib2.urlopen(url.get_url_with_query_params())
            resp_object = json.loads(resp.read())
            try:
                with open('data/%s.csv' % resp_object['result'][0]['hostname'], 'w') as fp:
                    for k, v in resp_object['result'][0]['timeSeriesValues'].items():
                        fp.write(','.join([str(k), str(v)]) + '\n')
            except IndexError:
                logger.log(ERROR, THREAD_ERROR_TEMPLATE % sys._current_frames()[currentThread().ident].f_locals)
            queue.task_done()
