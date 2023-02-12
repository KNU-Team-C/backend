terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project
  region      = var.region
  zone        = var.zone
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
        image = "docker.io/teamcknu/project_backend"
		startup_probe {
          tcp_socket {
            port = 5000
          }
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

# Allow unauthenticated users to invoke the service
resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.backend_app.location
  project  = google_cloud_run_service.backend_app.project
  service  = google_cloud_run_service.backend_app.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

output "service_url" {
  value = google_cloud_run_service.backend_app.status[0].url
}
