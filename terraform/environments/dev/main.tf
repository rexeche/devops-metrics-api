terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # For your sandbox, local state is fine.
  # In production you'd use S3 backend (like your Azure Storage backends at CRISP)
}

provider "aws" {
  region = var.region
}

module "ecr" {
  source          = "../../modules/ecr"
  repository_name = "devops-metrics-api"
  tags            = local.tags
}

module "eks" {
  source       = "../../modules/eks"
  cluster_name = "devops-lab-${var.environment}"
  region       = var.region
  environment  = var.environment
  tags         = local.tags
}

locals {
  tags = {
    Project     = "devops-interview-lab"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}
# test trigger