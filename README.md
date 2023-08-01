PROGRAMMING EXERCISE

Description:

This code package is a technical implementation comprising a code repository aimed at constructing a containerized Python program. The primary purpose of this program is to operate within a Kubernetes cluster and monitor the status of various pods. To determine the target status, the program accepts a parameter passed through an environment variable named POD_STATUS. The possible values for this parameter include: "Terminating," "Error," "Completed," "Running," or "CreateContainerConfigError."

Upon execution, the program generates a tabular representation (listing) of all pods that currently exist in the specified status, as identified by the POD_STATUS parameter.

The code package consist of three folder: Docker, PodStatusChecker-Chart and Test-Cases.


Project Requirement:

Step 1 – Program Development

The program was buiild and debugged in visual studio code. The python program was first test outside the kubenertes cluster running in minikube. 
 

Step 2 - Containerize

After the core functionality of the script was developed and validated, the next step involved containerizing it using a Dockerfile to produce a deployable image. This image was subsequently published to DockerHub for wider distribution and accessibility.

The Docker folder houses the necessary components for containerization. It contains the Dockerfile responsible for defining the build process and assembling the image. Additionally, the folder includes a requirements.txt file listing all the required Python dependencies, ensuring the proper environment for the script's execution. Finally, the folder contains the actual Python script, which constitutes the core logic of the application.

Run the following commands to build, tag and push the python program image:
    Builds the Image
    - docker build -t pod-status-checker ./Docker

    Tags the Image
    - docker tag pod-status-checker <RepoName>/pod-status-checker:latest

    Push to DockerHub
    - docker push <RepoName>/pod-status-checker:latest


Step 3  – Deploy your Container

The PodStatusChecker-Chark is a Helm chart designed to facilitate the deployment of essential manifest files responsible for running a Python container within a Kubernetes cluster. These manifest files encompass various components such as the service account, cluster role, cluster role binding, and deployment specifications.

The service account, cluster role, and cluster role binding play a pivotal role in granting necessary permissions to the program container, thereby enabling it to access and retrieve the status information of pods residing within the cluster. This setup ensures that the program operates with the required privileges to effectively obtain and list the status of pods, ensuring smooth and secure execution within the Kubernetes environment.

Run the following commands to deploy the python container in kubernetes cluster using helm charts:
    Validate the helm chart 
    - helm lint . 

    Ensure the values are getting substituted in the template
    - helm template . 

    check if there are any issues with the chart
    - helm install --dry-run pod-status-checker ./PodStatusChecker-Chart

    Deploy the manifest files to the cluster:
    - helm install pod-status-checker ./PodStatusChecker-Chart -f ./PodStatusChecker-Chart/values.yaml 

Step 4 - Testing

The Test-Cases folder consist of manifest files that simulate the deployment of pods in the kubernetes cluster with: Terminating, Error, Completed, Running, or CreateContainerConfigError statuses. 

Run the following commands to deploy the pods to simulate the Terminating, Error, Completed, Running, or CreateContainerConfigError pod statuses:
    
    kubectl apply -f completed.yaml
    kubectl apply -f CreateContainerConfigError.yaml
    kubectl apply -f error.yaml
    kubectl apply -f running.yaml
    kubectl apply -f terminating.yaml

Run the follwoing commands to test the designated pod status state:

    TEST-CASE 1: Terminating
        Update the PodStatus to "Terminating" in the values.yaml and save the changes
        - helm upgrade pod-status-checker PodStatusChecker-Chart -f ./PodStatusChecker-Chart/values.yaml 
        - kubectl delete pods terminating-pod
        - kubectl logs -f pod-status-checker
          NOTE: This command should output a listing of the pods in the Terminating state

    TEST-CASE 2: Error
        Update the PodStauts to "Error" in the values.yaml and save the changes
        - helm upgrade pod-status-checker PodStatusChecker-Chart -f ./PodStatusChecker-Chart/values.yaml
        - kubectl logs -f pod-status-checker
          NOTE: This command should output a listing of the pods in the Error state

    TEST-CASE 3: Completed
        Update the PodStauts to "Completed" in the values.yaml and save the changes
        - helm upgrade pod-status-checker PodStatusChecker-Chart -f ./PodStatusChecker-Chart/values.yaml
        - kubectl logs -f pod-status-checker
          NOTE: This command should output a listing of the pods in the Completed state

    TEST-CASE 4: Running
        Update the PodStauts to "Running" in the values.yaml and save the changes
        - helm upgrade pod-status-checker PodStatusChecker-Chart -f ./PodStatusChecker-Chart/values.yaml
        - kubectl logs -f pod-status-checker
          NOTE: This command should output a listing of the pods in the Running state

    TEST-CASE 5: CreateContainerConfigError
        Update the PodStauts to "CreateContainerConfigError" in the values.yaml and save the changes
        - helm upgrade pod-status-checker PodStatusChecker-Chart -f ./PodStatusChecker-Chart/values.yaml
        - kubectl logs -f pod-status-checker
          NOTE: This command should output a listing of the pods in the CreateContainerConfigError state
