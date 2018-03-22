##!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from joblib import Parallel, delayed

import utils
from utils import RG_TEMPLATE, resize_VM

"""
README:
1. Stop All in Ambari
2. Run this script
3. Change Ambari settings

curl 'http://localhost:8080/api/v1/clusters/Cluster/config_groups/2' -u admin:admin -H "X-Requested-By: ambari" -i  -X PUT --data '{"ConfigGroup":{"group_name":"MasterNode","description":"","tag":"YARN","hosts":[],"desired_configs":[]}}' --compressed
/var/lib/ambari-server/resources/scripts/configs.sh set localhost Cluster yarn-site yarn.nodemanager.resource.cpu-vcores 16
/var/lib/ambari-server/resources/scripts/configs.sh set localhost Cluster yarn-site yarn.scheduler.maximum-allocation-vcores 16
/var/lib/ambari-server/resources/scripts/configs.sh set localhost Cluster yarn-site yarn.nodemanager.resource.memory-mb 98304
/var/lib/ambari-server/resources/scripts/configs.sh set localhost Cluster yarn-site yarn.scheduler.maximum-allocation-mb 98304

4. Start All in Ambari
5. Change SparkContext settings

More workers:
    sc = get_spark_context(executorsPerNode=16, memoryPerExecutor=6144)
More memory per worker:
    sc = get_spark_context(executorsPerNode=8, memoryPerExecutor=12288)
Even more memory per worker (huge ALS workload maybe):
    sc = get_spark_context(executorsPerNode=4, memoryPerExecutor=24576)

"""

parser = argparse.ArgumentParser()
parser.add_argument("--user", action="store", help="account name, for example student1", required=True)
args = parser.parse_args()

STUDENT_NAME = args.user
RG_NAME = RG_TEMPLATE.format(STUDENT_NAME)
NEW_SIZE = "Standard_DS14_v2_Promo"  # Standard DS14 v2 Promo (16 cores, 112 GB memory)

Parallel(n_jobs=3, backend="threading")(
    delayed(resize_VM)("cluster{0}".format(idx), RG_NAME, NEW_SIZE) for idx in [1, 2, 3]
)

print "cluster1 public IP: {}".format(utils.get_public_ip("ip_cluster1", RG_NAME))
