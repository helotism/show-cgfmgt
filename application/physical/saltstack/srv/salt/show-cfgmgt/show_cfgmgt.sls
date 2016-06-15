backup file:
 cmd.file.copy:
   - tgt: {{ data['data']['id'] }}
   - arg:
     - {{ data['data']['path'] }}
     - {{ data['data']['path'] }}.bak
