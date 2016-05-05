#!/usr/bin/python

import os
from ansible.module_utils.basic import *

def create_test_file(name, content):
    with open(name, 'w') as f:
        f.write(content)

def delete_test_file(name):
    if os.path.exists(name):
        os.remove(name)

if __name__ == '__main__':
    module = AnsibleModule(
        argument_spec = dict(
            state = dict(default='present', choices=['present', 'absent']),
            name = dict(required=True),
            content = dict(type='str')))

    result = module.params.copy()
    result['changed'] = False

    if module.params['state'] == 'present':
        create_test_file(module.params['name'], module.params['content'])
        result['changed'] = True

    elif module.params['state'] == 'absent':
        delete_test_file(module.params['name'])
        result['changed'] = True

    module.exit_json(**result)
