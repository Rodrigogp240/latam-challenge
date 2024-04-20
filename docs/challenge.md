# Completing the LATAM_Challenge

## Introduction

This project focuses on developing a FastAPI-based API for predicting flight delays using the XGBoost machine learning algorithm.

## Part 1: Data Modeling

### Model Selection - XGBoost

For this project, XGBoost was chosen over Linear Regression due to its superior speed performance, especially with larger datasets. Although both XGBoost and Logistic Regression yield comparable results, XGBoost stands out in terms of computational efficiency under normal conditions.

### Creating the `DelayModel` Class

The `DelayModel` class serves as a central component for data preprocessing and model training:

- **Utility Class Creation:** A utility class was developed to streamline the preprocessing step, enhancing both efficiency and accuracy.
- **Integration of Save Feature:** The `fit` method incorporates a save feature, ensuring seamless model persistence for future use.
- **Implementation of Validation:** Validation mechanisms within the `predict` method prevent execution without a fitted model, enhancing robustness and reliability.

## Part 2: API Design

### API Integration

The trained XGBoost model and preprocessing steps were integrated into the FastAPI application's `/predict` endpoint. Key aspects include:

- **Validation Classes:** Two validation classes, `Flight` and `FlightList`, ensure data integrity by validating individual flight data entries and lists of flight data, respectively.

## Part 3: GCP Integration

In this section, we discuss the integration with Google Cloud Platform (GCP) and the rationale behind choosing Google Container Registry (GCR) and Artifact Registry (AR).

### Choice of Google Container Registry (GCR) and Artifact Registry (AR)

- **Google Container Registry (GCR):**
  - GCR provides secure storage and fast distribution for Docker container images. Its seamless integration with Cloud Build and Kubernetes Engine makes it an ideal choice for storing container images within the GCP ecosystem.

- **Artifact Registry (AR):**
  - AR offers advanced features such as vulnerability scanning and artifact versioning, making it suitable for storing Docker container images. Its fine-grained access control enhances security and reliability.

By leveraging GCR and AR, we ensure secure storage, efficient distribution, and easy access to Docker container images within the GCP environment.

## Part 4: DevOps

This section outlines the Continuous Integration (CI) and Continuous Delivery (CD) processes implemented for the project.

### Continuous Integration (CI)

The CI process ensures regular integration and testing of changes to the project codebase. Key steps include setting up the Python environment, caching dependencies, and running model and API tests using GitHub Actions.

### Continuous Delivery (CD)

CD automates the deployment of changes to the production environment. Upon completion of the CI workflow, authentication with Google Cloud, building and pushing the Docker container to Artifact Registry, and deploying the container to Cloud Run are executed.

These CI/CD processes automate testing, building, and deployment, ensuring the project's reliability, efficiency, and consistency throughout its development lifecycle.

## Conclusion

Overall, this project provided valuable insights into building a predictive API using machine learning and integrating it with cloud services. The experience gained underscores the importance of efficient data modeling, API design, and DevOps practices. I look forward to further exploring and refining these concepts in future projects.
