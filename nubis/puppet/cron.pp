$manage_command = "nubis-cron ${project_name}-manage /opt/${projectname}/venv/bin/python /var/www/${project_name}/manage.py refresh_events"

#Run manage.py every hour
cron::hourly { "${project_name}-manage":
  user    => $apache::params::user,
  command => $manage_command,
}
