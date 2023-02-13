terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }

    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.1"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project
  region      = var.region
  zone        = var.zone
}

provider "docker" {
  host = "npipe:////.//pipe//docker_engine"

  registry_auth {
    address  = "registry.hub.docker.com"
  }
}

# Pulls the Docker image
resource "docker_image" "backend_image" {
  name          = data.docker_registry_image.backend_image.name
  pull_triggers = [data.docker_registry_image.backend_image.sha256_digest]
}

data "docker_registry_image" "backend_image" {
  name = "teamcknu/backend:latest"
}

# Enables the Cloud Run API
resource "google_project_service" "run_api" {
  service = "run.googleapis.com"

  disable_on_destroy = true
}

# Creates Google Cloud Run app
resource "google_cloud_run_service" "backend_app" {
  name     = "backend-app"
  location = var.region
  template {
    spec {
      containers {
        image = docker_image.backend_image.name
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [
    google_project_service.run_api
  ]
}

# Allow unauthenticated users to invoke the service
data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.backend_app.location
  project  = google_cloud_run_service.backend_app.project
  service  = google_cloud_run_service.backend_app.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

output "service_url" {
  value = google_cloud_run_service.backend_app.status[0].url
}
