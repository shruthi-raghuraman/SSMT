from abc import ABCMeta, abstractstaticmethod
from flask import Blueprint,render_template
from flask import request
from flask.json import jsonify
from helper import helper
import json
import requests
import constants
import dateutil.parser as dp
from datetime import datetime, timedelta

utilObject=helper.Helper()

#Interface for query metering object
class IQueryMetering(metaclass = ABCMeta):
    @abstractstaticmethod
    def get_project_reports(projectName):
        """Interface"""

#Interface implementation for query metering object
class NamespaceCpuRequest(IQueryMetering):
    def __init__(self):
        pass

    def get_project_reports(self):

        #Retrieve frequency from query parameter
        frequency = request.args.get('frequency')
        if frequency == 'day':
            url = constants.METERING_ROUTE_NAMESPACE_CPU_REQUEST_DAILY
        elif frequency == 'week':
            url = constants.METERING_ROUTE_NAMESPACE_CPU_REQUEST_WEEKLY
        elif frequency == 'month':
            url = constants.METERING_ROUTE_NAMESPACE_CPU_REQUEST_MONTHLY

        headers = utilObject.getRequestHeader()
        r = requests.get(url, headers=headers, verify=False)

        #Retrieve all data
        input_json = r.text
        input_dict = json.loads(input_json)
        data = [x for x in input_dict]

        #Filter by query date
        period_start = request.args.get('start')
        input_date = dp.parse(request.args.get('start'))

        #Filter by time period specified
        if frequency == 'day':
            start = input_date
            end = input_date
        elif frequency == 'week':
            start = input_date - timedelta(days=input_date.weekday())
            end = start + timedelta(days=6)
        elif frequency == 'month':
            start = input_date.replace(day=1)
            end = input_date.replace(day=calendar.monthrange(input_date.year, input_date.month)[1])

        data = [x for x in data if (dp.parse(x['period_start']).replace(tzinfo=None) > start and dp.parse(x['period_end']).replace(tzinfo=None) < end)]

        output_dict = {}
        output_dict["reports"] = data
        output_dict["request_parameters"] = {"start": request.args.get('start'), "frequency": request.args.get('frequency')}
        if len(data) == 0:
            return jsonify(output_dict)
        else:
            return jsonify(output_dict)

class ListProject(IQueryMetering):
    def __init__(self):
        pass

    def get_project_reports(self):

        url = constants.METERING_ROUTE_LIST_ALL_PROJECTS
        headers = utilObject.getRequestHeader()
        r = requests.get(url, headers=headers, verify=False)

        #Retrieve all data
        input_json = r.text
        input_dict = json.loads(input_json)

        #Filter by date
        data = [x for x in input_dict if (x['period_start'] == period_start or x['period_end'] == period_end)]
        data = [x for x in data if x['namespace'] == project_name]

        if len(data) == 0:
            return "Report are not Generated. Please Wait until OpenShift Cluster Collect Metrics"
        else:
            return jsonify(data)

#Factory method
class QueryMeteringFactory():

    @staticmethod
    def retrieve_query(queryType):
        try:
            if queryType == "namespace_cpu_request":
                return NamespaceCpuRequest()
            elif queryType == "list_projects":
                return ListProject()
            raise AssertionError("Query Not Found")
        except AssertionError as _e:
            return _e
