# Define how Apache should be installed and configured
class { 'nubis_apache': }

class { 'apache::mod::wsgi':
  package_name => 'libapache2-mod-wsgi-py3',
  mod_path     => "${::apache::params::lib_path}/mod_wsgi.so",
}

#WSGI Setup for AirmoFront
apache::vhost { $project_name:
  serveradmin                 => 'webops@mozilla.com',
  default_vhost               => true,
  port                        => 80,
  docroot                     => "/var/www/${project_name}",
  wsgi_application_group      => '%{GLOBAL}',
  wsgi_daemon_process         => 'wsgi',
  wsgi_daemon_process_options => {
    processes    => '2',
    threads      => '15',
    display-name => '%{GROUP}',
    home         => "/var/www/${project_name}",
    python-home  => "/opt/${project_name}/venv",
  },
  wsgi_import_script          => "/var/www/${project_name}/airmozilla/wsgi_nubis.py",
  wsgi_import_script_options  => {
    process-group     => 'wsgi',
    application-group => '%{GLOBAL}',
  },
  wsgi_process_group          => 'wsgi',
  wsgi_script_aliases         => { '/' => "/var/www/${project_name}/airmozilla/wsgi_nubis.py" },

  custom_fragment             => "
    # Don't set default expiry on anything
    ExpiresActive Off

    # Clustered without coordination
    FileETag None

    # Mark internal traffic as not log-worthy
    SetEnvIfExpr \"-R '10.0.0.0/8' || -R '172.16.0.0/12' || -R '192.168.0.0/16' || -R '127.0.0.0/8'\" internal
  ",
  setenv => [
    'DJANGO_SETTINGS_MODULE airmozilla.settings_nubis',
  ],
  aliases                     => [
    {
      alias => '/static',
        path  => "/var/www/${project_name}/static",
    }
  ],

  block                       => ['scm'],
  setenvif                    => [
    'X-Forwarded-Proto https HTTPS=on',
  ],
  access_log_env_var          => '!internal',
  access_log_format           => '%a %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"',
  headers                     => [
    "set X-Nubis-Version ${project_version}",
    "set X-Nubis-Project ${project_name}",
    "set X-Nubis-Build   ${packer_build_name}",
  ],
  rewrites                    => [
    {
      comment      => 'HTTPS redirect',
      rewrite_cond => ['%{HTTP:X-Forwarded-Proto} =http'],
      rewrite_rule => ['. https://%{HTTP:Host}%{REQUEST_URI} [L,R=permanent]'],
    }
  ]
}
