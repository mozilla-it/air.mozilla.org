$manage_command = "/usr/local/bin/consul-do $(nubis-metadata NUBIS_PROJECT)-$(nubis-metadata NUBIS_ENVIRONMENT)-manage $(hostname) && nubis-cron ${project_name}-manage /opt/${project_name}/venv/bin/python /var/www/${project_name}/manage.py refresh_events"

$airmo_cron_enabled = true

if $airmo_cron_enabled {
  #Run manage.py every hour
  cron { "${project_name}-manage":
    user    => $apache::params::user,
    hour    => '*',
    minute  => '*/15',
    command => $manage_command,
  }
}
