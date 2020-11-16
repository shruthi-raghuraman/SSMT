# Bulk data trigger into Openshift Metering backend

#### Explore database and data structure within OCP
  - Set up code ready container and OpenShift Metering
  - Connect to Hive with the following command:
```
oc -n openshift-metering exec -it $(oc -n openshift-metering get pods -l app=hive,hive=server -o name | cut -d/ -f2) -c hiveserver2 -- beeline -u 'jdbc:hive2://127.0.0.1:10000/default;auth=noSasl'
```
  - View tables and table content within metering database

#### Modify load script to incorporate new data
  - Obtain bulk data that matches schema for data within the OCP
  - Create INSERT INTO statements for each datapoint and provide a .sql file
  - Obtain raw github link for the .sql file (Example github link: https://gist.githubusercontent.com/shruthi-raghuraman/eecda49f0741bf0ea12ce2f766f3a0bd/raw/ffe9b3f8b49cc77d57dc058d4372a494d266d135/namespace_cpu_request_hourly.sql)
  - Within load.sh, add the following lines
```sh
#Obtain the bulk data file
oc -n openshift-metering exec -it $(oc -n openshift-metering get pods -l app=hive,hive=server -o name | cut -d/ -f2) -c hiveserver2 -- curl -o <YOUR_INSERT_FILE.sql> <RAW GITHUB LINK>

#Load data into database from within container
oc -n openshift-metering exec -it $(oc -n openshift-metering get pods -l app=hive,hive=server -o name | cut -d/ -f2) -c hiveserver2 -- beeline -u 'jdbc:hive2://127.0.0.1:10000/default;auth=noSasl' -f <YOUR_INSERT_FILE.sql>
```
#### Run from within crc container
  - Using the primary readme, set up code ready containers with openshift metering
  - Create the targeted data report utilizing yaml files provided (can create custom yaml files as well). For example, for namespace-cpu-request-daily.yaml, utilize the following command:
```
oc create -f openshift-meteCring-templates/reports-templates/namespace-cpu-request-daily.yaml
```
  - Run load script to access database and load bulk insert statements within the table
  ```
  ./load.sh
  ```

#### Creating .sql INSERT INTO statements for bulk data
This can be done in many different ways. The following is a quick method to convert data points into INSERT statements that minimizes manual effort.
  - Set up DataGrip (these steps follow DataGrip but any other database management tool works) https://www.jetbrains.com/help/datagrip/quick-start-with-datagrip.html#step-3-write-your-code
  - Ensure bulk data collection is in csv file (if it is in json convert to csv https://json-csv.com/)
  - Once local database connection is set up, right click on schema -> Import Data From File -> Select .csv file -> OK
  - In the next menu, ensure column names and type are similar to how they appear within Openshift Metering database. Utilize the Data Preview shown for this and click Import.
  - Use built in extractor to extract and export data as INSERT INTO STATEMENTS (https://www.jetbrains.com/help/datagrip/export-data-in-ide.html#built-in-extractors)
  - Relabel table name within INSERT statement to reflect OCP metering tables. For example: for namespace-cpu-request-daily one insert statement should look like this
 ```
 INSERT INTO metering.`report_openshift_metering_namespace_cpu_request_daily` (namespace, period_end, period_start, pod_request_cpu_core_seconds) VALUES ('openshift-apiserver', '2020-10-15 14:00:00', '2020-10-15 13:00:00', 6);
```
  - This method outputs individual INSERT INTO statements that can be turned into one insert statement for all points.
