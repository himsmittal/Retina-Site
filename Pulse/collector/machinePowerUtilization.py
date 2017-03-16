from metricTs import MetricTs


class MachinePowerUtilization(MetricTs):
    def __init__(self, host, scheme):
        super(MachinePowerUtilization, self).__init__(host, scheme)
        self.host = host
        self.scheme = scheme
        self.params = {}
        self.path = '/v1/internal/metrics/powerConsumption'
