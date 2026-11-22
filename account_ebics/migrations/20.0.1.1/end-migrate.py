# Copyright 2026 Noviat.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openupgradelib import openupgrade

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """
    Remove account_ebics_batch module record and its meta-entries since this
    module is now merged into the base account_ebics module.
    """
    cr.execute("SELECT id FROM ir_module_module WHERE name = 'account_ebics_batch'")
    row = cr.fetchone()
    if not row:
        return
    old_id = row[0]
    openupgrade.logger.info(
        "account_ebics end-migrate: removing account_ebics_batch (id=%s)", old_id
    )
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["ir.model.data"]._module_data_uninstall(["account_ebics_batch"])
    openupgrade.logged_query(
        cr, "DELETE FROM ir_model_constraint WHERE module = %s", [old_id]
    )
    openupgrade.logged_query(
        cr, "DELETE FROM ir_model_relation WHERE module = %s", [old_id]
    )
    openupgrade.logged_query(cr, "DELETE FROM ir_module_module WHERE id = %s", [old_id])
    openupgrade.logged_query(
        cr,
        "DELETE FROM ir_model_data WHERE module = 'base'"
        " AND model = 'ir.module.module'"
        " AND name = 'module_account_ebics_batch'",
    )
