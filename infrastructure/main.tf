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

  backend "gcs" {
    bucket = "teamcknu-backend-bucket"
    prefix = "terraform/state"
  }
}

provider "google" {
  # credentials = file(var.credentials_file)
  project = var.project
  region  = var.region
  zone    = var.zone
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
  # host = "npipe:////.//pipe//docker_engine" # for Windows

  registry_auth {
    address = "registry.hub.docker.com"
  }
}

# Enables the Cloud Run API
resource "google_project_service" "run_api" {
  service = "run.googleapis.com"
}

# Creates Google Cloud Run app
resource "google_cloud_run_service" "backend_server" {
  name     = "backend-server-dev"
  location = var.region

  template {
    spec {
      containers {
        image = "teamcknu/backend:${var.docker_tag}"
        env {
          name = "DATABASE_URI"
          value_from {
            secret_key_ref {
              name = "companies-db-uri"
              key  = "latest"
            }
          }
        }
        env {
          name = "SECRET_KEY"
          value_from {
            secret_key_ref {
              name = "jwt-secret-key"
              key  = "latest"
            }
          }
        }
        env {
          name = "IMAGE_UPLOAD_API_URL"
          value_from {
            secret_key_ref {
              name = "image-upload-url"
              key  = "latest"
            }
          }
        }
        env {
          name = "IMAGE_UPLOAD_API_KEY"
          value_from {
            secret_key_ref {
              name = "image-upload-api-key"
              key  = "latest"
            }
          }
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [
    google_project_service.run_api,
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
  location = google_cloud_run_service.backend_server.location
  project  = google_cloud_run_service.backend_server.project
  service  = google_cloud_run_service.backend_server.name

  policy_data = data.google_iam_policy.noauth.policy_data

  depends_on = [
    google_cloud_run_service.backend_server
  ]
}

output "service_url" {
  value = google_cloud_run_service.backend_server.status[0].url
}
