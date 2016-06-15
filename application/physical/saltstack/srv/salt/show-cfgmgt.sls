The inotify beacon requires Pyinotify :
  pkg.installed:
    - name: python2-pyinotify

#/etc/salt/master.d/reactor.conf:
#  file.prepend:
#    - text:
#      - "reactor:"

/etc/salt/minion.d/beacons.conf:
  file.prepend:
    - text:
      - "beacons:"

setup the virtual python environment:
  virtualenv.managed:
    - name: /opt/helotism/show-cfgmgt_venv
    - python: python3
    - system_site_packages: False
    - pip_pkgs:
      - gpiozero
      - pyyaml
      - RPi.GPIO

The python script itself:
  file.managed:
    - name: /opt/helotism/show-cfgmgt_venv/app.py
    - user: root
    - group: root
    - mode: 744
    - source: salt:///show-cfgmgt/app.py
    - require:
      - virtualenv: /opt/helotism/show-cfgmgt_venv

And its config file:
  file.managed:
    - name: /opt/helotism/show-cfgmgt_venv/config.yml
    - user: root
    - group: root
    - mode: 744
#    - contents:
#      - "performance: gold"
    - source: salt:///show-cfgmgt/config.yml
    - require:
      - virtualenv: /opt/helotism/show-cfgmgt_venv
      - file: /opt/helotism/show-cfgmgt_venv/app.py

enable the systemd service:
  service.running:
    - name: helotism-show-cfgmgt.service
    - enable: true
    - provider: systemd
    - watch:
      - file: /opt/helotism/show-cfgmgt_venv/config.yml
    - require:
      - file: /etc/systemd/system/helotism-show-cfgmgt.service

place the systemd unit file in the correct folder:
  file.managed:
    - name: /etc/systemd/system/helotism-show-cfgmgt.service
    - source: salt:///show-cfgmgt/helotism-show-cfgmgt.service.sample

