#Install Python 3.4
class { 'python' :
    version    => 'latest',
    pip        => 'present',
}

python::requirements { '/var/www/project1/requirements.txt' :
    proxy      => 'http://proxy.domain.com:3128',
    owner      => 'appuser',
    group      => 'apps',
}


#
#package { 'composer':
#  ensure => 'latest',
#}
#
### Install PHP composer extensions
#exec { 'composer':
#    command     => 'composer install --no-dev --verbose',
#    cwd         => "/var/www/${project_name}",
#    path        => '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
#    environment => [
#        'HOME=/tmp',
#    ],
#    require     => [
#      Class['apache::mod::php'],
#      Package['php-memcache'],
#      Package['php-mysql'],
#      Package['php-mbstring'],
#      Package['php-xml'],
#    ],
#}
#
## Use Nubis's autoconfiguration hooks to trigger out config reloads
#
#include nubis_configuration
#
#nubis::configuration { $project_name:
#  format => 'php',
#}
#
#file { [ '/etc/php', '/etc/php/7.0', '/etc/php/7.0/apache2', '/etc/php/7.0/apache2/conf.d' ]:
#  ensure => directory,
#  owner  => root,
#  group  => root,
#  mode   => '0744',
#}
#
#file { "/etc/php/7.0/apache2/conf.d/30-${project_name}.ini":
#  ensure => file,
#  owner  => root,
#  group  => root,
#  mode   => '0744',
#  source => 'puppet:///nubis/files/php.ini',
#}
#
#file { "/data/${project_name}/php_sessions":
#  ensure => directory,
#  owner  => www-data,
#  group  => www-data,
#  mode   => '0733',
#}
