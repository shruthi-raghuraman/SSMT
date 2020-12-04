from flask import Blueprint,render_template
from flask import request
from flask.json import jsonify
from helper import helper
import json
import requests
import constants
import dateutil.parser as dp

utilObject=helper.Helper()

def get_project_reports(project_name, url):
    headers = utilObject.getRequestHeader()
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

def list_project_runtime_search():
    url = constants.METERING_ROUTE_LIST_ALL_PROJECTS
    headers = utilObject.getRequestHeader()
    r = requests.get(url, headers=headers, verify=False)
    input_json = r.text
    input_dict = json.loads(input_json)
    output_dict = [x for x in input_dict if x['period_start'] >= period_start]
    data = [x for x in output_dict if x['period_end'] <= period_end]
    list_key_value = _countNumberOfHours(data)
    return jsonify(list_key_value)

def _countNumberOfHours(input_dict):
    ht=dict()
    for x in input_dict:
        if x['namespace'] in ht:
            ht[x['namespace']] += 1
        else:
            ht[x['namespace']] = 1
    list_key_value = [ dict(namespace=k, activation_time=v) for k, v in ht.items() ]
    return list_key_value
