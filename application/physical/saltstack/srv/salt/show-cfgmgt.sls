Making sure Python3 is installed:
  pkg.installed:
    - name: python

The inotify beacon requires Pyinotify :
  pkg.installed:
    - name: python2-pyinotify

#/etc/salt/master.d/reactor.conf:
#  file.prepend:
#    - text:
#      - "reactor:"

/etc/salt/minion.d/90_beacons.conf:
  file.prepend:
    - text:
      - "beacons:"

Adding the inotify section:
  file.append:
    - name: /etc/salt/minion.d/90_beacons.conf
    - source: salt:///show-cfgmgt/beacons.conf
#    - require:
#      - file: /etc/salt/minion.d/90_beacons.conf

Fixing a current bug in salt:
  file.replace:
    - name: /usr/lib/python2.7/site-packages/salt/states/virtualenv_mod.py
    - pattern: formar
    - repl: format

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
#    - source: salt:///colorfader.py
    - source: salt:///buttonpress-colorcycler.py
    - require:
      - virtualenv: /opt/helotism/show-cfgmgt_venv

And its config file:
  file.managed:
    - name: /opt/helotism/show-cfgmgt_venv/config.yml
    - user: root
    - group: root
    - mode: 744
    - source: salt:///show-cfgmgt/config.yml
    - require:
      - virtualenv: /opt/helotism/show-cfgmgt_venv
      - file: /opt/helotism/show-cfgmgt_venv/app.py

And its performance config file:
  file.managed:
    - name: /opt/helotism/show-cfgmgt_venv/performance.yml
    - user: root
    - group: root
    - mode: 744
#    - contents:
#      - performance: platinum
    - source: salt:///show-cfgmgt/performance.yml
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
      - file: /opt/helotism/show-cfgmgt_venv/performance.yml
      - file: /opt/helotism/show-cfgmgt_venv/app.py
    - require:
      - file: /etc/systemd/system/helotism-show-cfgmgt.service

place the systemd unit file in the correct folder:
  file.managed:
    - name: /etc/systemd/system/helotism-show-cfgmgt.service
    - source: salt:///show-cfgmgt/helotism-show-cfgmgt.service.sample

