# k8s_pod_status_checker.py

import os
import time
import sys
from kubernetes import client, config

def get_pods_in_status(namespace, status):
    config.load_incluster_config()  # Use in-cluster configuration

    v1 = client.CoreV1Api()

    pods = v1.list_namespaced_pod(namespace)
    filtered_pods = [pod for pod in pods.items if pod.status.phase == status]

    return filtered_pods

def print_pod_table(pods):
    print(f"{'POD NAME':40}{'STATUS':15}")
    print("="*60)
    for pod in pods:
        print(f"{pod.metadata.name:40}{pod.status.phase:15}")
    sys.stdout.flush()

if __name__ == "__main__":
    pod_status = os.environ.get("POD_STATUS", "Running")
    namespace = "default"  # Update this if you want to check in a specific namespace

    while True:
        try:
            pods_in_status = get_pods_in_status(namespace, pod_status)
            print(f"List of Pods in '{pod_status}' status:")
            print_pod_table(pods_in_status)
        except Exception as e:
            print(f"Error occurred: {e}")

        # Wait for 60 seconds before checking again
        time.sleep(2)