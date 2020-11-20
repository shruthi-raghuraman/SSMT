#!/usr/bin/env bash


#Obtain bulk data file: namespace_cpu_request_daily
oc -n openshift-metering exec -it $(oc -n openshift-metering get pods -l app=hive,hive=server -o name | cut -d/ -f2) -c hiveserver2 -- curl -o namespace_cpu_request_daily.sql https://gist.githubusercontent.com/shruthi-raghuraman/2af7b6892f3fec1d030ff11777ac2cea/raw/fad4da0880c9812d813a3dbe8641121f7edee594/namespace_cpu_request_daily.sql

#Obtain bulk data file: namespace_cpu_request_hourly
oc -n openshift-metering exec -it $(oc -n openshift-metering get pods -l app=hive,hive=server -o name | cut -d/ -f2) -c hiveserver2 -- curl -o namespace_cpu_request_hourly.sql https://gist.githubusercontent.com/shruthi-raghuraman/eecda49f0741bf0ea12ce2f766f3a0bd/raw/ffe9b3f8b49cc77d57dc058d4372a494d266d135/namespace_cpu_request_hourly.sql

#Load data into database from within container
oc -n openshift-metering exec -it $(oc -n openshift-metering get pods -l app=hive,hive=server -o name | cut -d/ -f2) -c hiveserver2 -- beeline -u 'jdbc:hive2://127.0.0.1:10000/default;auth=noSasl' -f namespace_cpu_request_daily.sql

#Load data into database from within container
oc -n openshift-metering exec -it $(oc -n openshift-metering get pods -l app=hive,hive=server -o name | cut -d/ -f2) -c hiveserver2 -- beeline -u 'jdbc:hive2://127.0.0.1:10000/default;auth=noSasl' -f namespace_cpu_request_hourly.sql
