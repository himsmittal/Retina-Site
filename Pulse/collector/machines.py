from urlBuilder import UrlBuilder
import urllib2, json


class Machines(object):
    def __init__(self, host, scheme):
        self.host = host
        self.scheme = scheme
        self.path = '/api/v1/machines'
        self.params = {'size': 100}
        self.machines = []
        self.total_machines = None

    def get_machines(self, queue):
        while True:
            self.params['page'] = queue.get()
            url = UrlBuilder(self.host, self.path, self.params, self.scheme)
            resp = urllib2.urlopen(url.get_url_with_query_params())
            for item in json.loads(resp.read())['result']:
                self.machines.append((item['id'], item['hostname']))
            queue.task_done()

    def list_machines(self):
        return self.machines

    def get_total_machines(self):
        url = UrlBuilder(self.host, self.path, self.params, self.scheme)
        resp = urllib2.urlopen(url.get_url_with_query_params())
        self._set_total_machines(json.loads(resp.read())['meta']['totalRecords'])

    def set_page_size(self, x):
        try:
            int(x)
        except ValueError:
            raise BaseException('Page size should be numeric.')
        self._set_param('size', int(x))

    def _set_total_machines(self, x):
        try:
            int(x)
        except ValueError:
            raise BaseException('Total Machines size should be numeric.')
        self.total_machines = int(x)

    def _set_param(self, key, value):
        self.params[key] = value

    def _add_machine(self, x):
        self.machines.append(x)
