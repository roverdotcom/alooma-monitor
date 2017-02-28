import alooma
import datadog
import datetime
import os
import time

ALOOMA_USERNAME = os.environ.get('ALOOMA_USERNAME')
ALOOMA_PASSWORD = os.environ.get('ALOOMA_PASSWORD')
DATADOG_API_KEY = os.environ.get('DATADOG_API_KEY')
MINUTES_SLEEP = 10
SECONDS_SLEEP = MINUTES_SLEEP * 60


api = alooma.Alooma(
    hostname='app.alooma.com',
    port=443,
    username=ALOOMA_USERNAME,
    password=ALOOMA_PASSWORD,
)

datadog.initialize(api_key=DATADOG_API_KEY)


def posix_timestamp():
    d = datetime.datetime.now()
    return str(int(time.mktime(d.timetuple())))


def send_metric(data):
    for d in data:
        metric_name = "alooma.{}".format(d['target'].lower())
        values = d['datapoints']

        for x in values:
            x.reverse()

        for v in values:
            v[0] = str(v[0])
            v[1] = float(0 if v[1] is None else v[1])

        values = [tuple(x) for x in values]

        print metric_name
        print values

        for v in values:
            print v
            result = datadog.api.Metric.send(
                metric=metric_name,
                points=v,
                type='gauge',
            )
            yield result


metrics = alooma.METRICS_LIST
metrics.remove('CPU_USAGE')
metrics.remove('MEMORY_CONSUMED')
metrics.remove('MEMORY_LEFT')


while True:
    for m in metrics:
        data = api.get_metrics_by_names(m, MINUTES_SLEEP)
        print "Sending {}".format(m)
        result = send_metric(data)

        for r in result:
            import pprint; pprint.pprint(r)

    inputs = api.get_inputs()
    num_inputs = len(inputs)
    result = datadog.api.Metric.send(
        metric='alooma.num_inputs',
        points=[(posix_timestamp(), num_inputs)],
        type='gauge',
    )

    print "Sleeping for {}m".format(MINUTES_SLEEP)
    time.sleep(SECONDS_SLEEP)
