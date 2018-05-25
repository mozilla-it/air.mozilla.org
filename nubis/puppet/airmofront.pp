#Install Python 3.4
class { 'python' :
    version => 'python3',
    pip     => true,
    dev     => true,
}

python::requirements { "/var/www/${project_name}/requirements.txt" :
  require =>  Class['python'],
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
  owner   => $apache::params::user,
  group   => $apache::params::group,
  require => [
    Class['nubis_apache'],
  ],
}

file { "/var/www/${project_name}/static/scss":
  ensure  => 'directory',
  owner   => $apache::params::user,
  group   => $apache::params::group,
  require => [
    Class['nubis_apache'],
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

