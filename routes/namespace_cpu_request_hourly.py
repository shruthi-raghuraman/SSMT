from flask import Blueprint,render_template
from flask import request
from flask.json import jsonify
from helper import helper
import json
import requests
import constants
import dateutil.parser as dp

namespace_cpu_request_hourly = Blueprint("namespace_cpu_request_hourly",__name__)
utilObject=helper.Helper()

@namespace_cpu_request_hourly.route('/<project_name>/standard')
def get_project_reports(project_name):
    headers = utilObject.getRequestHeader()
    url = constants.METERING_ROUTE_NAMESPACE_CPU_REQUEST_HOURLY
    r = requests.get(url, headers=headers, verify=False)
    period_start = request.args.get('start')
    input_json = r.text
    input_dict = json.loads(input_json)

    data = [x for x in input_dict]
    start_date = dp.parse(request.args.get('start'))
    data = [x for x in data if dp.parse(x['period_start']).replace(tzinfo=None) > start_date]

    output_dict = {}
    output_dict["reports"] = data
    output_dict["request_parameters"] = {"start": request.args.get('start'), "frequency": request.args.get('frequency')}
    if len(data) == 0:
        return "Report are not Generated. Please Wait until OpenShift Cluster Collect Metrics"
    else:
        return jsonify(output_dict)
