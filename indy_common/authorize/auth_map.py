from typing import Dict

from indy_common.authorize.auth_actions import AuthActionAdd, AuthActionEdit
from indy_common.authorize.auth_constraints import AuthConstraint, AuthConstraintOr
from indy_common.constants import TRUST_ANCHOR, POOL_CONFIG, VALIDATOR_INFO, POOL_UPGRADE, POOL_RESTART, NODE, \
    CLAIM_DEF, SCHEMA, NYM, ROLE, NETWORK_MONITOR, AUTH_RULE
from plenum.common.constants import TRUSTEE, STEWARD, VERKEY

IDENTITY_OWNER = ''
roles = [IDENTITY_OWNER, NETWORK_MONITOR, TRUST_ANCHOR, STEWARD, TRUSTEE]

edit_role_actions = {}  # type: Dict[str, Dict[str, AuthActionEdit]]
for role_from in roles:
    edit_role_actions[role_from] = {}
    for role_to in roles:
        edit_role_actions[role_from][role_to] = AuthActionEdit(txn_type=NYM,
                                                               field=ROLE,
                                                               old_value=role_from,
                                                               new_value=role_to)

add_new_trustee = AuthActionAdd(txn_type=NYM,
                                field=ROLE,
                                value=TRUSTEE)

add_new_steward = AuthActionAdd(txn_type=NYM,
                                field=ROLE,
                                value=STEWARD)

add_new_trust_anchor = AuthActionAdd(txn_type=NYM,
                                     field=ROLE,
                                     value=TRUST_ANCHOR)

add_new_network_monitor = AuthActionAdd(txn_type=NYM,
                                        field=ROLE,
                                        value=NETWORK_MONITOR)

add_new_identity_owner = AuthActionAdd(txn_type=NYM,
                                       field=ROLE,
                                       value=IDENTITY_OWNER)

key_rotation = AuthActionEdit(txn_type=NYM,
                              field=VERKEY,
                              old_value='*',
                              new_value='*')

add_schema = AuthActionAdd(txn_type=SCHEMA,
                           field='*',
                           value='*')

edit_schema = AuthActionEdit(txn_type=SCHEMA,
                             field='*',
                             old_value='*',
                             new_value='*')

add_claim_def = AuthActionAdd(txn_type=CLAIM_DEF,
                              field='*',
                              value='*')

edit_claim_def = AuthActionEdit(txn_type=CLAIM_DEF,
                                field='*',
                                old_value='*',
                                new_value='*')

adding_new_node = AuthActionAdd(txn_type=NODE,
                                field='services',
                                value='[\'VALIDATOR\']')

demote_node = AuthActionEdit(txn_type=NODE,
                             field='services',
                             old_value='[\'VALIDATOR\']',
                             new_value='[]')

promote_node = AuthActionEdit(txn_type=NODE,
                              field='services',
                              old_value='[]',
                              new_value='[\'VALIDATOR\']')

change_node_ip = AuthActionEdit(txn_type=NODE,
                                field='node_ip',
                                old_value='*',
                                new_value='*')

change_node_port = AuthActionEdit(txn_type=NODE,
                                  field='node_port',
                                  old_value='*',
                                  new_value='*')

change_client_ip = AuthActionEdit(txn_type=NODE,
                                  field='client_ip',
                                  old_value='*',
                                  new_value='*')

change_client_port = AuthActionEdit(txn_type=NODE,
                                    field='client_port',
                                    old_value='*',
                                    new_value='*')

change_bls_key = AuthActionEdit(txn_type=NODE,
                                field='blskey',
                                old_value='*',
                                new_value='*')

start_upgrade = AuthActionAdd(txn_type=POOL_UPGRADE,
                              field='action',
                              value='start')

cancel_upgrade = AuthActionEdit(txn_type=POOL_UPGRADE,
                                field='action',
                                old_value='start',
                                new_value='cancel')

pool_restart = AuthActionAdd(txn_type=POOL_RESTART,
                             field='action',
                             value='*')

pool_config = AuthActionEdit(txn_type=POOL_CONFIG,
                             field='action',
                             old_value='*',
                             new_value='*')

auth_rule = AuthActionEdit(txn_type=AUTH_RULE,
                           field='*',
                           old_value='*',
                           new_value='*')

validator_info = AuthActionAdd(txn_type=VALIDATOR_INFO,
                               field='*',
                               value='*')

anyone_can_add_nym = AuthActionAdd(txn_type=NYM,
                                   field=ROLE,
                                   value='*')

anyone_can_add_schema = AuthActionAdd(txn_type=SCHEMA,
                                      field='*',
                                      value='*')

anyone_can_add_claim_def = AuthActionAdd(txn_type=CLAIM_DEF,
                                         field='*',
                                         value='*')

anyone_can_edit_nym = AuthActionEdit(txn_type=NYM,
                                     field=ROLE,
                                     old_value='*',
                                     new_value='*')

anyone_can_edit_schema = AuthActionEdit(txn_type=SCHEMA,
                                        field='*',
                                        old_value='*',
                                        new_value='*')

anyone_can_edit_claim_def = AuthActionEdit(txn_type=CLAIM_DEF,
                                           field='*',
                                           old_value='*',
                                           new_value='*')

# Anyone constraint
anyone_constraint = AuthConstraint(role='*',
                                   sig_count=1)

# Owner constraint
owner_constraint = AuthConstraint(role='*',
                                  sig_count=1,
                                  need_to_be_owner=True)

# Steward owner constraint
steward_owner_constraint = AuthConstraint(STEWARD, 1, need_to_be_owner=True)

# One Trustee constraint
one_trustee_constraint = AuthConstraint(TRUSTEE, 1)

# Steward or Trustee constraint
steward_or_trustee_constraint = AuthConstraintOr([AuthConstraint(STEWARD, 1),
                                                  AuthConstraint(TRUSTEE, 1)])

# Trust Anchor, Steward or Trustee constraint
trust_anchor_or_steward_or_trustee_constraint = AuthConstraintOr([AuthConstraint(TRUSTEE, 1),
                                                                  AuthConstraint(STEWARD, 1),
                                                                  AuthConstraint(TRUST_ANCHOR, 1)])

# Trustee or owner steward
trustee_or_owner_steward = AuthConstraintOr([AuthConstraint(TRUSTEE, 1),
                                             AuthConstraint(STEWARD, 1, need_to_be_owner=True)])

auth_map = {
    add_new_trustee.get_action_id(): one_trustee_constraint,
    add_new_steward.get_action_id(): one_trustee_constraint,
    add_new_trust_anchor.get_action_id(): steward_or_trustee_constraint,
    add_new_network_monitor.get_action_id(): steward_or_trustee_constraint,
    add_new_identity_owner.get_action_id(): trust_anchor_or_steward_or_trustee_constraint,
    key_rotation.get_action_id(): owner_constraint,
    add_schema.get_action_id(): trust_anchor_or_steward_or_trustee_constraint,
    edit_schema.get_action_id(): AuthConstraint(None, 1),
    add_claim_def.get_action_id(): trust_anchor_or_steward_or_trustee_constraint,
    edit_claim_def.get_action_id(): owner_constraint,
    adding_new_node.get_action_id(): steward_owner_constraint,
    demote_node.get_action_id(): trustee_or_owner_steward,
    promote_node.get_action_id(): trustee_or_owner_steward,
    change_node_ip.get_action_id(): steward_owner_constraint,
    change_node_port.get_action_id(): steward_owner_constraint,
    change_client_ip.get_action_id(): steward_owner_constraint,
    change_client_port.get_action_id(): steward_owner_constraint,
    change_bls_key.get_action_id(): steward_owner_constraint,
    start_upgrade.get_action_id(): one_trustee_constraint,
    cancel_upgrade.get_action_id(): one_trustee_constraint,
    pool_restart.get_action_id(): one_trustee_constraint,
    pool_config.get_action_id(): one_trustee_constraint,
    auth_rule.get_action_id(): one_trustee_constraint,
    validator_info.get_action_id(): AuthConstraintOr([AuthConstraint(TRUSTEE, 1),
                                                      AuthConstraint(STEWARD, 1),
                                                      AuthConstraint(NETWORK_MONITOR, 1)])
}

# Edit Trustee:
auth_map_trustee = {
    edit_role_actions[TRUSTEE][TRUSTEE].get_action_id(): owner_constraint,
    edit_role_actions[TRUSTEE][STEWARD].get_action_id(): one_trustee_constraint,
    edit_role_actions[TRUSTEE][TRUST_ANCHOR].get_action_id(): one_trustee_constraint,
    edit_role_actions[TRUSTEE][NETWORK_MONITOR].get_action_id(): one_trustee_constraint,
    edit_role_actions[TRUSTEE][IDENTITY_OWNER].get_action_id(): one_trustee_constraint,
}
auth_map.update(auth_map_trustee)

# Edit Steward
auth_map_steward = {
    edit_role_actions[STEWARD][TRUSTEE].get_action_id(): one_trustee_constraint,
    edit_role_actions[STEWARD][STEWARD].get_action_id(): owner_constraint,
    edit_role_actions[STEWARD][TRUST_ANCHOR].get_action_id(): one_trustee_constraint,
    edit_role_actions[STEWARD][NETWORK_MONITOR].get_action_id(): one_trustee_constraint,
    edit_role_actions[STEWARD][IDENTITY_OWNER].get_action_id(): one_trustee_constraint,
}
auth_map.update(auth_map_steward)

# Edit Trust Anchor
auth_map_trust_anchor = {
    edit_role_actions[TRUST_ANCHOR][TRUSTEE].get_action_id(): one_trustee_constraint,
    edit_role_actions[TRUST_ANCHOR][STEWARD].get_action_id(): one_trustee_constraint,
    edit_role_actions[TRUST_ANCHOR][TRUST_ANCHOR].get_action_id(): owner_constraint,
    edit_role_actions[TRUST_ANCHOR][NETWORK_MONITOR].get_action_id(): one_trustee_constraint,
    edit_role_actions[TRUST_ANCHOR][IDENTITY_OWNER].get_action_id(): one_trustee_constraint,
}
auth_map.update(auth_map_trust_anchor)

# Edit Network Monitor
auth_map_network_monitor = {
    edit_role_actions[NETWORK_MONITOR][TRUSTEE].get_action_id(): one_trustee_constraint,
    edit_role_actions[NETWORK_MONITOR][STEWARD].get_action_id(): one_trustee_constraint,
    edit_role_actions[NETWORK_MONITOR][TRUST_ANCHOR].get_action_id(): steward_or_trustee_constraint,
    edit_role_actions[NETWORK_MONITOR][NETWORK_MONITOR].get_action_id(): owner_constraint,
    edit_role_actions[NETWORK_MONITOR][IDENTITY_OWNER].get_action_id(): steward_or_trustee_constraint,
}
auth_map.update(auth_map_network_monitor)

# Edit Identity Owner
auth_map_identity_owner = {
    edit_role_actions[IDENTITY_OWNER][TRUSTEE].get_action_id(): one_trustee_constraint,
    edit_role_actions[IDENTITY_OWNER][STEWARD].get_action_id(): one_trustee_constraint,
    edit_role_actions[IDENTITY_OWNER][TRUST_ANCHOR].get_action_id(): steward_or_trustee_constraint,
    edit_role_actions[IDENTITY_OWNER][NETWORK_MONITOR].get_action_id(): steward_or_trustee_constraint,
    edit_role_actions[IDENTITY_OWNER][IDENTITY_OWNER].get_action_id(): owner_constraint,
}
auth_map.update(auth_map_identity_owner)

# Special rules, activated when ANYONE_CAN_WRITE set to True
anyone_can_write_map = {anyone_can_add_nym.get_action_id(): anyone_constraint,
                        anyone_can_add_schema.get_action_id(): anyone_constraint,
                        anyone_can_add_claim_def.get_action_id(): owner_constraint,
                        anyone_can_edit_nym.get_action_id(): anyone_constraint,
                        anyone_can_edit_schema.get_action_id(): anyone_constraint,
                        anyone_can_edit_claim_def.get_action_id(): owner_constraint}
