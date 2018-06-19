$manage_command =  "nubis-cron ${project_name}-manage /var/www/airmofront/manage.py refresh_events"

#Run manage.py every hour
cron::hourly { "${project_name}-manage":
  user    => $apache::params::user,
  command => $manage_command,
}
