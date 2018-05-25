#Install Python 3.4
class { 'python' :
    version => 'system',
    pip     => true,
    dev     => true,
}

python::requirements { "/var/www/${project_name}/requirements.txt" :
  require =>  Class['python'],
}

file { "/var/www/${project_name}/airmo/settings.py":
  ensure => file,
  source => 'puppet:///nubis/files/settings.py'
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

