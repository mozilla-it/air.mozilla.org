$manage_command =  "consul-do $(nubis-metadata NUBIS_PROJECT)-$(nubis-metadata NUBIS_ENVIRONMENT)-manage $(hostname) && nubis-cron ${project_name}-manage /opt/${project_name}/venv/bin/python /var/www/${project_name}/manage.py refresh_events"

#Run manage.py every hour
cron::hourly { "${project_name}-manage":
  user    => $apache::params::user,
  command => $manage_command,
}
