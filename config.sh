export OS_LIST_ALL_PROJECTS_URL="http://metering-openshift-metering.apps-crc.testing/api/v1/reports/get?name=list-all-projects-v1-hourly&namespace=openshift-metering&format=json"

export OS_NAMESPACE_CPU_REQUEST_HOURLY="http://metering-openshift-metering.apps-crc.testing/api/v1/reports/get?name=namespace-cpu-request-hourly&namespace=openshift-metering&format=json"

export OS_NAMESPACE_CPU_REQUEST_DAILY="http://metering-openshift-metering.apps-crc.testing/api/v1/reports/get?name=namespace-cpu-request-daily&namespace=openshift-metering&format=json"

export OS_NAMESPACE_CPU_REQUEST_WEEKLY="http://metering-openshift-metering.apps-crc.testing/api/v1/reports/get?name=namespace-cpu-request-weekly&namespace=openshift-metering&format=json"

export OS_NAMESPACE_CPU_REQUEST_MONTHLY="http://metering-openshift-metering.apps-crc.testing/api/v1/reports/get?name=namespace-cpu-request-monthly&namespace=openshift-metering&format=json"

export OS_OPENSHIFT_TOKEN="$(oc whoami -t)"
