# Install Nginx if not already installed
class nginx {
  package { 'nginx':
    ensure => installed,
  }
}

# Create necessary directories
file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']:
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create test HTML file
file { '/data/web_static/releases/test/index.html':
  content => '<html><body>Holberton School Test Page</body></html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

# Create symbolic link to current release
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Update Nginx configuration
class nginx_config {
  include nginx

  # Serve content from /data/web_static/current under the URI /hbnb_static
  file { '/etc/nginx/sites-available/default':
    content => "server {
      listen 80 default_server;
      listen [::]:80 default_server;

      location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
      }

      location / {
        add_header X-Served-By $hostname;
      }
    }",
    require => Class['nginx'],
    notify  => Service['nginx'],
  }
}

# Restart Nginx
service { 'nginx':
  ensure     => running,
  enable     => true,
  hasrestart => true,
  require    => Class['nginx_config'],
}

