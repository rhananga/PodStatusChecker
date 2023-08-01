# Kubernetes Pod Status Checker

This repository contains a Python program designed to monitor the status of pods within a Kubernetes cluster. The program is containerized using Docker, making it easy to deploy and execute within a Kubernetes environment. Additionally, we provide Helm charts to facilitate the deployment of the containerized program and a set of test cases to validate its functionality.

## Description

The primary objective of this code package is to monitor the status of pods within a Kubernetes cluster. The status to be monitored is determined by the value of the environment variable `POD_STATUS`, which can take one of the following values: "Terminating," "Error," "Completed," "Running," or "CreateContainerConfigError."

Upon execution, the program generates a tabular representation (listing) of all pods that currently exist in the specified status, as identified by the `POD_STATUS` parameter.

## Project Structure

The repository is organized into three main folders:

1. **Docker**: This folder contains the necessary components for containerizing the Python program. It includes the Dockerfile responsible for defining the build process and assembling the Docker image. The `requirements.txt` file lists all the required Python dependencies to ensure a proper execution environment. Finally, the folder contains the core logic of the application in the form of a Python script.

2. **PodStatusChecker-Chart**: This folder contains a Helm chart designed to streamline the deployment process of the Python program within a Kubernetes cluster. The chart includes various manifest files, such as service account, cluster role, cluster role binding, and deployment specifications.

3. **Test-Cases**: This folder contains manifest files simulating the deployment of pods in different statuses within the Kubernetes cluster. These test cases help verify the program's ability to correctly identify and list pods with specific statuses.

## Project Requirements

### Step 1 – Program Development

The Python program was developed and debugged using Visual Studio Code. It was initially tested outside the Kubernetes cluster using Minikube to ensure its core functionality.

### Step 2 - Containerize

Once the core functionality of the Python script was validated, it was containerized using a Dockerfile to create a deployable Docker image. The Docker image was then published to DockerHub for wider distribution and accessibility.

To build, tag, and push the Python program image, use the following commands:

```bash
# Builds the Image
docker build -t pod-status-checker ./Docker

# Tags the Image
docker tag pod-status-checker <RepoName>/pod-status-checker:latest

# Push to DockerHub
docker push <RepoName>/pod-status-checker:latest
```

### Step 3 – Deploy your Container

The Helm chart, `PodStatusChecker-Chart`, assists in deploying the essential manifest files required to run the Python container within a Kubernetes cluster. These manifest files include the service account, cluster role, cluster role binding, and deployment specifications.

The service account, cluster role, and cluster role binding grant the necessary permissions to the program container, enabling it to access and retrieve the status information of pods within the cluster. This setup ensures that the program operates with the required privileges to effectively obtain and list the status of pods, ensuring smooth and secure execution within the Kubernetes environment.

To deploy the Python container in the Kubernetes cluster using the Helm chart, use the following commands:

```bash
# Validate the helm chart
helm lint .

# Ensure the values are getting substituted in the template
helm template .

# Check if there are any issues with the chart
helm install --dry-run pod-status-checker ./PodStatusChecker-Chart

# Deploy the manifest files to the cluster
helm install pod-status-checker ./PodStatusChecker-Chart -f ./PodStatusChecker-Chart/values.yaml
```

### Step 4 - Testing

The `Test-Cases` folder contains manifest files that simulate the deployment of pods with various statuses within the Kubernetes cluster. These test cases ensure the correct functionality of the Python program in different scenarios.

To deploy the pods and test the designated pod status states, use the following commands:

```bash
# Deploy the pods to simulate different pod statuses
kubectl apply -f Test-Cases/completed.yaml
kubectl apply -f Test-Cases/CreateContainerConfigError.yaml
kubectl apply -f Test-Cases/error.yaml
kubectl apply -f Test-Cases/running.yaml
kubectl apply -f Test-Cases/terminating.yaml

# Test Case 1: Terminating
# Update the PodStatus to "Terminating" in the values.yaml and save the changes
helm upgrade pod-status-checker PodStatusChecker-Chart -f ./PodStatusChecker-Chart/values.yaml
kubectl delete pods terminating-pod
kubectl logs -f pod-status-checker
# NOTE: This command should output a listing of the pods in the Terminating state

# Test Case 2: Error
# Update the PodStatus to "Error" in the values.yaml and save the changes
helm upgrade pod-status-checker PodStatusChecker-Chart -f ./PodStatusChecker-Chart/values.yaml
kubectl logs -f pod-status-checker
# NOTE: This command should output a listing of the pods in the Error state

# Test Case 3: Completed
# Update the PodStatus to "Completed" in the values.yaml and save the changes
helm upgrade pod-status-checker PodStatusChecker-Chart -f ./PodStatusChecker-Chart/values.yaml
kubectl logs -f pod-status-checker
# NOTE: This command should output a listing of the pods in the Completed state

# Test Case 4: Running
# Update the PodStatus to "Running" in the values.yaml and save the changes
helm upgrade pod-status-checker PodStatusChecker-Chart -f ./PodStatusChecker-Chart/values.yaml
kubectl logs -f pod-status-checker
# NOTE: This command should output a listing of the pods in the Running state

# Test Case 5: CreateContainerConfigError
# Update the PodStatus to "CreateContainerConfigError" in the values.yaml and save the changes
helm upgrade pod-status-checker PodStatusChecker-Chart -f ./PodStatusChecker-Chart/values.yaml
kubectl logs -f pod-status-checker
# NOTE: This command should output a listing of the pods in the CreateContainerConfigError state
```