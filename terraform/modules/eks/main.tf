# VPC for the cluster
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.cluster_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.region}a", "${var.region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = true  # Cost savings for sandbox
  enable_dns_hostnames = true

  # Tags required for EKS
  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }
  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }

  tags = var.tags
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.29"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # Public endpoint for kubectl access (fine for sandbox)
  cluster_endpoint_public_access = true
  enable_cluster_creator_admin_permissions = true

  # Managed node group — the actual EC2 instances running your pods
  eks_managed_node_groups = {
    default = {
      instance_types = ["t3.small"]  # ~$0.0416/hr, cheapest usable for K8s
      min_size       = 1
      max_size       = 2
      desired_size   = 1  # Keep it small for costs

      labels = {
        environment = var.environment
      }
    }
  }

  tags = var.tags
}