from flask import Blueprint,render_template
from flask import request
from flask.json import jsonify
from helper import helper
import json
import requests
import constants
import dateutil.parser as dp
from routes.QueryMeteringFactory import *

list_projects = Blueprint("list_projects",__name__)
namespace_cpu_request = Blueprint("namespace_cpu_request",__name__)


utilObject=helper.Helper()
#/reports/standard?start=2020-12-04&frequency=week

@namespace_cpu_request.route('/standard')
def get_namespace_cpu_request():
    #Specify api endpoint
    QUERY = QueryMeteringFactory.retrieve_query("namespace_cpu_request")
    #Retrieve report
    return QUERY.get_project_reports()

@list_projects.route('/standard')
def list_project_runtime_search():
    #Specify api endpoint
    QUERY = QueryMeteringFactory.retrieve_query("list_projects")
    #Retrieve report
    return QUERY.get_project_reports()
