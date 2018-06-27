#Install Python 3.4
class { 'python' :
    version    => 'python3',
    pip        => true,
    dev        => true,
    virtualenv => true,
}

file { "/opt/${project_name}":
  ensure => directory,
}

python::virtualenv { "/opt/${project_name}/venv":
  ensure  => present,
  version => '3',
  require => [
    Class['python'],
    File["/opt/${project_name}"],
  ]
}

python::requirements { "/var/www/${project_name}/requirements.txt" :
  virtualenv => "/opt/${project_name}/venv",
  require    =>  [
    Class['python'],
    Python::Virtualenv["/opt/${project_name}/venv"],
  ]
}

file { "/var/www/${project_name}/airmozilla/settings_nubis.py":
  ensure => present,
  source => 'puppet:///nubis/files/settings.py'
}

file { "/var/www/${project_name}/airmozilla/wsgi_nubis.py":
  ensure => present,
  source => 'puppet:///nubis/files/wsgi.py'
}

file { "/var/www/${project_name}/static/CACHE":
  ensure  => 'directory',
  owner   => 'www-data',
  group   => 'www-data',
  require => [
    Class['apache'],
  ],
}

file { "/var/www/${project_name}/static/scss":
  ensure  => 'directory',
  owner   => 'www-data',
  group   => 'www-data',
  require => [
    Class['apache'],
  ],
}

# Help manage.py know what settings file to look at
file { "/var/www/${project_name}/.env":
  ensure  => present,
  content => "
DJANGO_SETTINGS_MODULE=airmozilla.settings_nubis
",
  owner   => root,
  group   => root,
  mode    => '0644',
}

file { "/usr/local/bin/${project_name}-update":
  ensure => present,
  source => 'puppet:///nubis/files/update',
  owner  => root,
  group  => root,
  mode   => '0755',
}

include nubis_configuration

nubis::configuration { $project_name:
  format => 'sh',
  reload => "/usr/local/bin/${project_name}-update"
}

file { '/etc/apache2/airmolegacyurlsmap.txt':
  ensure  => present,
  source  => 'puppet:///nubis/files/airmolegacyurlsmap.txt',
  owner   => root,
  group   => root,
  mode    => '0644',
  require => [
    Class['apache'],
  ],
}
