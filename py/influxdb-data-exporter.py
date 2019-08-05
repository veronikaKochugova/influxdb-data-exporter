from influxdb import InfluxDBClient
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY

# TODO make it configurable
HOST = "10.247.113.117"
PORT = 8086
USERNAME = 'admin'
PASSWORD = 'password'
DBNAME = 'pravega'


def print_points(result):
    for point in result:
        print(point)


class CustomCollector(object):
    def collect(self):
        yield GaugeMetricFamily('my_gauge', 'Help text', value=7)
        c = CounterMetricFamily('my_counter_total', 'Help text', labels=['foo'])
        c.add_metric(['bar'], 1.7)
        c.add_metric(['baz'], 3.8)
        yield c


REGISTRY.register(CustomCollector())

client = InfluxDBClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD, database=DBNAME)
query = 'show measurements;'

result = client.query(query).get_points()
measurements = list()
for point in result:
    measurements.append(point["name"])
print(measurements)

query = 'select * from ' + measurements[0] + " where time > now() - 1m ;"
result = client.query(query).get_points()

print_points(result)

start_http_server(9999)
