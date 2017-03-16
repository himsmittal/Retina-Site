from metricTs import MetricTs


class MachineCpu(MetricTs):
    def __init__(self, host, scheme):
        super(MachineCpu, self).__init__(host, scheme)
        self.host = host
        self.scheme = scheme
        self.params = {}
        self.path = '/v1/internal/metrics/percentCpuUtilization'
