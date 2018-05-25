#Install Python 3.4
class { 'python' :
    version => 'python3',
    pip     => true,
    dev     => true,
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
  require =>  [
    Class['python'],
    Python::Virtualenv["/opt/${project_name}/venv"],
  ]
}

file { "/var/www/${project_name}/airmozilla/settings.py":
  ensure => present,
  source => 'puppet:///nubis/files/settings.py'
}

file { "/var/www/${project_name}/airmozilla/settings_live.py":
  ensure => present,
  source => 'puppet:///nubis/files/settings_live.py'
}

file { "/var/www/${project_name}/static/CACHE":
  ensure  => 'directory',
  owner   => "www-data",
  group   => "www-data",
  require => [
    Class['apache'],
  ],
}

file { "/var/www/${project_name}/static/scss":
  ensure  => 'directory',
  owner   => "www-data",
  group   => "www-data",
  require => [
    Class['apache'],
  ],
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

