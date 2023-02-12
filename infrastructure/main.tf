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
  project 	= var.project
  region  	= var.region
  zone    	= var.zone
}

resource "google_compute_network" "vpc_network" {
  name = "teamc-network"
}

resource "docker_container" "backend_container" {
  image = "backend:latest"
  name  = "backend"
  restart = "always"
  ports {
    internal = 5000
    external = 8080
  }
}

