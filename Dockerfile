FROM python:2.7

RUN pip install jinja2 alooma datadog && mkdir /rover

COPY . /rover

WORKDIR /rover
CMD ["./go.sh"]
