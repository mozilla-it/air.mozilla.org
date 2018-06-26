provider “aws” {
 region = “${var.region}”
}

module "worker" {
  source            = "github.com/nubisproject/nubis-terraform//worker?ref=v2.2.0"
  region            = "${var.region}"
  environment       = "${var.environment}"
  account           = "${var.account}"
  service_name      = "${var.service_name}"
  purpose           = "webserver"
  instance_type     = "t2.small"
  ami               = "${var.ami}"
  elb               = "${module.load_balancer.name}"
  nubis_sudo_groups = "team_webops,nubis_global_admins"

  # EC2 for testing
  # ELB once done
  health_check_type = "ELB"

  # CPU utilisation based autoscaling (with good defaults)
  scale_load_defaults = true
  min_instances       = 2
  max_instances       = 32
}

module "load_balancer" {
  source               = "github.com/nubisproject/nubis-terraform//load_balancer?ref=v2.2.0"
  region               = "${var.region}"
  environment          = "${var.environment}"
  account              = "${var.account}"
  service_name         = "${var.service_name}"
  ssl_cert_name_prefix = "${var.service_name}"
}

module "database" {
  source                 = "github.com/nubisproject/nubis-terraform//database?ref=develop"
  region                 = "${var.region}"
  environment            = "${var.environment}"
  account                = "${var.account}"
  service_name           = "${var.service_name}"
  client_security_groups = "${module.worker.security_group}"
  engine                 = "postgres"
  name                   = "airmotest"
  username               = "airmotester"
}

module "dns" {
  source       = "github.com/nubisproject/nubis-terraform//dns?ref=v2.2.0"
  region       = "${var.region}"
  environment  = "${var.environment}"
  account      = "${var.account}"
  service_name = "${var.service_name}"
  target       = "${module.load_balancer.address}"
}

module "cache" {
  source                 = "github.com/nubisproject/nubis-terraform//cache?ref=v2.2.0"
  region                 = "${var.region}"
  environment            = "${var.environment}"
  account                = "${var.account}"
  service_name           = "${var.service_name}"
  client_security_groups = "${module.worker.security_group}"
}
