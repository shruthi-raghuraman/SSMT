from routes.query_metering_functions import *
from flask import Blueprint,render_template
from flask import request
from flask.json import jsonify
from helper import helper
import json
import requests
import constants
import dateutil.parser as dp

list_projects = Blueprint("list_projects",__name__)
list_runtime = Blueprint("list_runtime",__name__)
namespace_cpu_request_hourly = Blueprint("namespace_cpu_request_hourly",__name__)
namespace_cpu_request_daily = Blueprint("namespace_cpu_request_daily",__name__)

utilObject=helper.Helper()

@list_projects.route('/<project_name>/standard')
def get_list_projects(project_name):
    return get_project_reports(project_name, constants.METERING_ROUTE_LIST_ALL_PROJECTS)

@list_runtime.route('/<project_name>/standard')
def list_project_runtime_search(project_name):
    return get_project_reports(project_name, constants.METERING_ROUTE_LIST_RUNTIME)

@list_projects.route('/<project_name>/standard')
def get_list_projects(project_name):
    return get_project_reports(project_name, constants.METERING_ROUTE_LIST_ALL_PROJECTS)

@namespace_cpu_request_hourly.route('/<project_name>/standard')
def get_list_projects(project_name):
    return get_project_reports(project_name, constants.METERING_ROUTE_NAMESPACE_CPU_REQUEST_HOURLY)

@namespace_cpu_request_daily.route('/<project_name>/standard')
def get_list_projects(project_name):
    return get_project_reports(project_name, constants.METERING_ROUTE_NAMESPACE_CPU_REQUEST_DAILY)
