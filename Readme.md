# Flask Application Deployment in Kubernetes (K8s)

This project demonstrates the development, containerization, and deployment of a Flask web application in a local Kubernetes (K8s) environment using Docker Desktop's integrated Kubernetes.

## Overview

The Flask application includes basic endpoints and is containerized using Docker. 
It's designed to run locally in a Kubernetes cluster managed by Docker Desktop. 
This guide covers the setup process, deployment steps, and security best practices.

## Prerequisites

Before you begin, ensure you have the following installed and properly configured:

- [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10): Upgrade to WSL version 2 for enhanced performance and compatibility with Docker Desktop.
- [Docker Desktop](https://www.docker.com/products/docker-desktop) with Kubernetes enabled
- [kubectl](https://kubernetes.io/docs/tasks/tools/) command-line tool configured to interact with your Kubernetes cluster


## Deliverables:
Source Code: Flask app (app.py)
Dockerfile: Docker configuration (Dockerfile)
K8s YAML Files: Deployment and Service (flask-app-deployment.yaml, flask-app-service.yaml)
Documentation: Readme.md file included

## Directory Structure

```bash

/flask-app
    |--- Dockerfile
    |--- app.py
    |--- flask-app-deployment.yaml
    |--- flask-app-service.yaml

Dockerfile: Defines the Docker container for the Flask application.
app.py: The Flask application code.
flask-app-deployment.yaml: Kubernetes deployment configuration.
flask-app-service.yaml: Kubernetes service configuration.

```

## (1)Develop a Flask Application

Create a simple Flask web app with the following requirements:
- The app should have at least 2 endpoints/routes.
- Implement proper error handling and logging.


```python

# Import the necessary modules for the Flask application and logging.
from flask import Flask, jsonify
import logging

# Initialize the Flask application and configure logging to debug level.
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Define the home endpoint. Logs a message and returns a welcome message when accessed.
@app.route('/')
def home():
    app.logger.info('Home endpoint was reached')
    return "Welcome to the Flask App"

# Define the status endpoint. Logs a message and returns the running status in JSON format when accessed.
@app.route('/status')
def status():
    app.logger.info('Status endpoint was reached')
    return jsonify({"status": "running"})

# Error handling for 404 errors. Logs the error and returns a JSON response with the error details.
@app.errorhandler(404)
def page_not_found(e):
    app.logger.error('Page not found: %s', (e))
    return jsonify(error=404, text=str(e)), 404

# Run the application if this script is executed as the main program.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


```

The Flask application fulfills requirements:

1. **Multiple Endpoints/Routes**:
    - **Home (`'/'`)**: Serves as the primary entry point, returning a welcoming message and facilitating initial user interaction.
    - **Status (`'/status'`)**: Offers real-time app status in JSON format, crucial for system health monitoring.

2. **Error Handling and Logging**:
    - **404 Error Management**: Efficiently handles non-existent routes by providing clear JSON responses, enhancing user comprehension of issues.
    - **Logging Mechanism**: Employs DEBUG-level logging to comprehensively record pivotal events, such as access to endpoints and 404 errors, ensuring thorough monitoring and ease of troubleshooting.





##  (2)Containerize the Flask App

Dockerize the Flask app with these requirements:
- Create a Dockerfile for the Flask app.
- Ensure the app runs in a Docker container locally.
- Build the Docker image and run the container.

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages
RUN pip install --no-cache-dir flask

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "./app.py"]
```

How it addresses each requirement:

1. **Create a Dockerfile for the Flask app**:
   - **Base Image**: Utilizes `python:3.8-slim`, an official Python runtime, as the parent image, ensuring a lightweight and reliable foundation.
   - **Working Directory**: Sets `/usr/src/app` as the working directory inside the container, providing a structured and predictable environment for the application.

2. **Ensure the app runs in a Docker container locally**:
   - **Application Files**: Copies the current directory's contents into the container, ensuring all necessary files (`app.py`, etc.) are available in the working directory.
   - **Dependencies**: Installs required packages (Flask) using `pip`, preparing the environment with necessary libraries.
   - **Port Exposure**: Exposes port `5000`, aligning with the Flask app's default port, making the application accessible from outside the container.
   - **Execution Command**: Defines the command to run `app.py` when the container starts, activating the Flask server and ensuring the app is operational upon container launch.

3. **Document steps to build and run the container**:
   - **Build Container**: Execute `docker build -t flask-app .` to create the Docker container, tagging it as `flask-app`.
   - **Run Container**: Use `docker run -p 4000:5000 flask-app` to start the container, mapping the host's port 4000 to the container's port 5000, ensuring the Flask app is accessible locally.


## (3)K8s Deployment

Deploy the Flask app on K8s with these requirements:
- Create K8s manifest (YAML files) for deployment and service.
- Describe the process of deploying the app on the K8s cluster.
- Include considerations for scalability and high availability.

## flask-app-deployment.yaml:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-app
        image: flask-app:latest
        #The app runs in a Docker container locally if image exist
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 5000

```
The `flask-app-deployment.yaml` sets up a Kubernetes Deployment with 3 replicas of the Flask app for scalability and high availability. 
It uses the local `flask-app:latest` image, following the `IfNotPresent` policy to avoid redundant image pulls, and exposes port `5000`. 



## flask-app-service.yaml:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  selector:
    app: flask-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer


```
The `flask-app-service.yaml` file defines a Kubernetes Service for the Flask application, facilitating network access. 
It selects pods with the label `app: flask-app` and routes external TCP traffic on port `80` to the target port `5000` on the pods. 
The Service is of type `LoadBalancer`, ensuring efficient distribution of incoming traffic among the pods for optimal load handling.


The K8s Deployment process effectively meets the requirements for deploying the Flask app:

1. **Create K8s Manifests**:
    - **Deployment (flask-app-deployment.yaml)**: Defines a Deployment with 3 replicas, ensuring multiple instances for load distribution and redundancy. It references the `flask-app:latest` image and sets `imagePullPolicy: IfNotPresent`, indicating the local image will be used if available. The container port `5000` is exposed for app communication.
    - **Service (flask-app-service.yaml)**: Defines a Service with a `LoadBalancer` type, facilitating external access to the app. It maps port `80` to the app's port `5000`, ensuring the app can be reached via standard HTTP requests.

2. **Deploying the App on the K8s Cluster**:
    - Apply the manifests to the Kubernetes cluster using `kubectl apply -f flask-app-deployment.yaml` and `kubectl apply -f flask-app-service.yaml`. This creates the necessary Deployment and Service resources in the cluster.

3. **Considerations for Scalability and High Availability**:
    - **Replicas**: Setting replicas to 3 in the Deployment ensures that multiple instances of the app are available, providing high availability and supporting load balancing.
    - **LoadBalancer Service**: The LoadBalancer type in the Service definition evenly distributes incoming traffic among the pods, ensuring efficient handling of requests and improving the app's scalability and reliability.




## Assumptions:

1. **Environment Setup**:
   - It's assumed that the development environment includes Docker Desktop with Kubernetes enabled and that `kubectl` is configured to interact with the local Kubernetes cluster.
   - The system is presumed to have WSL (Windows Subsystem for Linux) upgraded to version 2 for better interoperability with Docker Desktop.

2. **Flask Application Development**:
   - The Flask app is assumed to have a minimal setup with at least two endpoints (`'/'` and `'/status'`), primarily for demonstration and health-check purposes.
   - Proper error handling for common HTTP errors (like 404) is assumed to be part of the Flask app's basic requirements.

3. **Containerization with Docker**:
   - It's assumed that the Flask app is containerized using a Dockerfile based on the lightweight `python:3.8-slim` image and that all necessary files are present in the build context.
   - The Docker container is expected to run locally, and the Dockerfile includes instructions to expose the appropriate port (`5000`) and run the application upon container startup.

4. **Kubernetes Deployment**:
   - The deployment process assumes the availability of Kubernetes manifest files (`flask-app-deployment.yaml` and `flask-app-service.yaml`) to define the app's deployment and service within the cluster.
   - It's assumed that the deployment strategy considers scalability and high availability, specifying multiple replicas and using a LoadBalancer to distribute incoming traffic.

5. **Local Deployment Specifics**:
   - The `imagePullPolicy: IfNotPresent` assumption ensures that local images are used for deployment, avoiding unnecessary image pulls from remote registries.
   - The assumption that the LoadBalancer service in Docker Desktop exposes the application on `localhost`, making it accessible for testing and interaction.



## Instructions on How to Set Up and Run the Flask Application

### Building the Flask Application

1. **Pull the Python Base Image**:
   - Navigate to your project directory.
   - Pull the Python base image:
```bash
     docker pull python:3.8-slim
```

2. **Build the Docker Image**:
   - Build your Flask app's Docker image:
```bash
     docker build -t flask-app:latest .
```

### Running the Flask Application Locally

1. **Start the Flask Application**:
   - Run the Docker container using the image you've built, mapping port `4000` on your host to port `5000` in the container:
 ```bash
     docker run -p 4000:5000 flask-app:latest
```

### Testing the Flask Application Locally

1. **Access the Application**:
   - Open your web browser and go to `http://localhost:4000/`.
   - Alternatively, use `curl` to test the application endpoints:
```bash
     curl http://localhost:4000/
     curl http://localhost:4000/status
```

2. **Check Running Containers**:
   - List the running Docker containers:
```bash
     docker ps
```

3. **Stop the Flask Application**:
   - Stop the running Docker container using its container ID:
```bash
     docker stop <container-id>
```

### Deployment in Kubernetes

1. **Prepare Kubernetes**:
   - Ensure Kubernetes is enabled in Docker Desktop.
   - Start the Kubernetes node on Docker Desktop.

2. **Verify Kubernetes Setup**:
   - Check that your `kubectl` context is set to `docker-desktop`:
```bash
     kubectl config current-context
 ```
   - Verify the health and info of your cluster and nodes:
```bash
     kubectl cluster-info
     kubectl get nodes
```

3. **Deploy the Application**:
   - Apply the Kubernetes manifests to create the deployment and service:
```bash
     kubectl apply -f flask-app-deployment.yaml
     kubectl apply -f flask-app-service.yaml
```

4. **Check Deployment Status**:
   - Monitor the status of deployments, pods, and services:
```bash
     kubectl get deployments
     kubectl get pods
     kubectl get services
```
   - Access the application at `http://localhost` (port `80`).

5. **Test the Application in Kubernetes**:
   - Use `curl` to verify the application is running correctly:
```bash
     curl http://localhost:80/
     curl http://localhost:80/status
```

### Clean Up Resources in Kubernetes

1. **Delete Deployments**:
   - Remove the deployment(s), which also deletes the managed pods:
```bash
     kubectl delete deployment flask-app-deployment
```

2. **Delete Services**:
   - Remove the service(s) you created:
```bash
     kubectl delete service flask-app-service
```

3. **Confirm Deletion**:
   - Stop the Kubernetes node on Docker Desktop.

4. **Confirm Deletion**:
   - Ensure that the deployments and services are deleted:
```bash
     kubectl get deployments
     kubectl get services
```
   - If there are other resources you've created (like ConfigMaps, Secrets, etc.), delete those as well.

By following these structured steps, you can set up, run, test, and manage the Flask application both locally with Docker and within a Kubernetes environment.

## Challenges

During the setup and deployment process, a few challenges were encountered and successfully addressed, ensuring a smooth development environment:

1. **WSL Upgrade**: Upgraded Windows Subsystem for Linux (WSL) to version 2. 
This upgrade was essential for enhanced performance and better compatibility with Docker Desktop, especially concerning file system performance and networking features.

2. **Docker Desktop Installation**: Installed Docker Desktop to leverage its seamless integration with WSL 2. 
This integration was crucial for ensuring a consistent and efficient containerization experience, allowing the use of Docker commands natively within the WSL environment and simplifying the management of Kubernetes clusters.
