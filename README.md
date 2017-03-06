```yaml
- hosts: openwisp2
  become: "{{ become | default('yes') }}"
  roles:
    - DimPolissiou.openwisp2
  vars:
    openwisp2_shared_secret: <PLEASE_CHANGE_ME>  # put any value of your liking
    openwisp2_cas_server: "http://127.0.0.1/cas/"
    openwisp2_cas_affiliation: "userPrincipalName"
    openwisp2_collectd_rrd_dir: "/var/lib/collectd/rrd/"
```
