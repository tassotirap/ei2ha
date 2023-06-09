# EI-2-HA
Home Assistant - Electric Ireland Integration

## Requirements
- Mariadb Addon https://github.com/home-assistant/addons/blob/master/mariadb/DOCS.md

## Installation
- Copy all the file to \config\custom_components\ei2ha
- Change the file config.py with our Electric Ireland information and Home Assistant information
- Add this to your configuration.yaml file
```
template:
  - sensor:
      - name: "Electric Ireland"
        state: "0"
        unit_of_measurement: "kWh"
        device_class: energy
        state_class: measurement
        availability: "false"
```

## Automation 
- Create a new automation with
```
alias: Electric Ireland Updater
description: ""
trigger:
  - platform: time
    at: "08:00:00"
condition: []
action:
  - service: ei2ha.update
    data: {}
mode: single
```
