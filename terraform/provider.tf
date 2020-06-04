#---
# Provider Configuration
#---

provider "aws" {
  region  = "us-west-2"
}

terraform {
  required_version = "~> 0.12"

  backend "s3" {
    # Bucket naming best practices https://mana.mozilla.org/wiki/display/SRE/Terraform
    bucket = "airmozilla-state-783633885093"
    key    = "terraform.tfstate"
    region = "us-west-2"
  }
}
