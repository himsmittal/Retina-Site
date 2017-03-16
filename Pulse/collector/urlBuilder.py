
class UrlBuilder(object):
    def __init__(self, host, path, parms, scheme='http'):
        self.host = host
        self.path = path
        self.params = parms
        self.scheme = scheme

    def get_base_url(self):
        return '%s://%s' % (self.scheme, self.host)

    def get_url_with_path(self):
        return '%s://%s%s' % (self.scheme, self.host, self.path)

    def get_url_with_query_params(self):
        if len(self.params) > 0:
            query_tokens = []
            for key, value in self.params.items():
                query_tokens.append(key+'=')
                query_tokens.append(str(value)+'&')
            query = "".join(query_tokens)[:-1]
            return '%s://%s%s?%s' % (self.scheme, self.host, self.path, query)
        else:
            return self.get_url_with_path()
