variable "account" {
  default = "appsvcs-airmofront"
}

variable "region" {
  default = "us-west-2"
}

variable "environment" {
  default = "stage"
}

variable "service_name" {
  default = "appsvcs-airmofront"
}

variable "ami" {}

variable "db_instance_class" {
  type = "map"

  default = {
    stage = "db.t2.micro"
    prod  = "db.r3.large"
    any   = "db.t2.micro"
  }
}
