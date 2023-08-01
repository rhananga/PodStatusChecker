# k8_pod_status_checker.py

import os
import sys
import time
from kubernetes import client, config

def get_pods_by_status(status):
    config.load_incluster_config()  # running in a Kubernetes cluster

    v1 = client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces(watch=False)

    pods_in_status = []
    for pod in pods.items:
        if pod.status.phase == status:
            pods_in_status.append(
                {
                    #"Namespace": pod.metadata.namespace,
                    "Name": pod.metadata.name,
                    "Status": pod.status.phase,
                }
            )
        else:
            for container_status in pod.status.container_statuses:
                if container_status.state.terminated and container_status.state.terminated.reason == status:
                    pods_in_status.append(
                        {
                            #"Namespace": pod.metadata.namespace,
                            "Name": pod.metadata.name,
                            "Status": status,
                        }
                    )
                elif container_status.state.waiting and container_status.state.waiting.reason == status:
                    pods_in_status.append(
                        {
                            #"Namespace": pod.metadata.namespace,
                            "Name": pod.metadata.name,
                            "Status": status,
                        }
                    )

    return pods_in_status

def print_pods_table(pods):
    if pods:
        print(f"\n\nPODS IN {pod_status} STATE :")
        print(f"{'POD NAME':40}{'STATE':15}")
        print("="*60)
        for pod in pods:
            print(f"{pod['Name']:40}{pod['Status']:15}")
        sys.stdout.flush()
    else:
        print(f"\nNO PODS FOUND IN THE {pod_status} STATE \n")
        sys.stdout.flush()

if __name__ == "__main__":
    while True:
        pod_status = os.environ.get("POD_STATUS", "Running")
        pods = get_pods_by_status(pod_status)
        print_pods_table(pods)
        time.sleep(2)  # Query every 2 second
