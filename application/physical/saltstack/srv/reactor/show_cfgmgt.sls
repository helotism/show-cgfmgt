backup file:
 cmd.file.copy:
   - tgt: {{ data['data']['id'] }}
   - arg:
     - {{ data['data']['path'] }}
     - {{ data['data']['path'] }}.bak

#apply the full state file again:
#  local.state.apply
#   - tgt: {{ data['data']['id'] }}
#   - arg:
#     - show-cfgmnt
