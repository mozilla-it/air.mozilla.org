# Discover Consul settings
module "consul" {
  source       = "github.com/nubisproject/nubis-terraform//consul?ref=v2.2.0"
  region       = "${var.region}"
  environment  = "${var.environment}"
  account      = "${var.account}"
  service_name = "${var.service_name}"
}

# Configure our Consul provider, module can't do it for us
provider "consul" {
  address    = "${module.consul.address}"
  scheme     = "${module.consul.scheme}"
  datacenter = "${module.consul.datacenter}"
}

# Publish our outputs into Consul for our application to consume
resource "consul_keys" "config" {
  key {
    path   = "${module.consul.config_prefix}/ENVIRONMENT"
    value  = "${var.environment}"
    delete = true
  }

  key {
    path   = "${module.consul.config_prefix}/SITE_URL"
    value  = "${module.dns.fqdn}"
    delete = true
  }

  key {
    path   = "${module.consul.config_prefix}/SECRET_KEY"
    value  = "${random_id.secret_key.b64_url}"
    delete = true
  }

  key {
    path   = "${module.consul.config_prefix}/Memcached"
    value  = "${module.cache.endpoint}"
    delete = true
  }
}

resource "random_id" "secret_key" {
  byte_length = 64
}
