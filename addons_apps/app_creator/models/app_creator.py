# -*- coding: utf-8 -*-
import os
import traceback
import textwrap
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger("app_creator")

# Fixed target path (as requested)
BASE_PATH = r"D:\odoo18 for\odoo\addons_apps"

def _safe_write_file(path, content):
    """Helper that logs file writes and raises on failure."""
    _logger.info("app_creator: Attempting to write file: %s", path)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        _logger.info("app_creator: File written: %s", path)
    except Exception as e:
        _logger.error("app_creator: Failed to write file %s: %s", path, e)
        raise

class AppCreator(models.Model):
    _name = "app.creator"
    _description = "App Creator (instrumented)"

    name = fields.Char(string="App Name", required=True)
    technical_name = fields.Char(string="Technical Name", required=True)
    description = fields.Text(string="Description")
    author = fields.Char(string="Author", default="Unknown")
    version = fields.Char(string="Version", default="1.0.0")
    created_path = fields.Char(string="Created Module Path", readonly=True)

    @api.model
    def _model_cr_test(self):
        """
        This method runs once when model registry is created.
        It writes a log so we can confirm models are loaded at server start.
        """
        try:
            _logger.info("app_creator: model_cr executed - app_creator model loaded")
        except Exception:
            # Do not block server if logging fails
            pass

    def _render_manifest(self, vals):
        return textwrap.dedent("""\
        # -*- coding: utf-8 -*-
        {{
            "name": "{name}",
            "version": "{version}",
            "summary": "{summary}",
            "description": "{description}",
            "author": "{author}",
            "category": "Uncategorized",
            "license": "AGPL-3",
            "depends": ["base"],
            "data": [
                "security/security.xml",
                "security/ir.model.access.csv",
                "views/{tech}_views.xml",
            ],
            "installable": True,
            "application": False,
            "auto_install": False,
        }}
        """).format(
            name=vals['name'],
            version=vals['version'],
            summary=(vals['description'] or "")[:120].replace('"', "'"),
            description=(vals['description'] or "").replace('"""', "'"),
            author=vals['author'],
            tech=vals['technical_name'],
        )

    def _render_init_py(self):
        return "# -*- coding: utf-8 -*-\nfrom . import models\n"

    def _render_models_init(self):
        return "# -*- coding: utf-8 -*-\nfrom . import models\n"

    def _render_models_py(self, technical):
        cls_name = technical.capitalize() if technical else "Test"
        return textwrap.dedent(f"""\
        # -*- coding: utf-8 -*-
        from odoo import models, fields

        class {cls_name}Test(models.Model):
            _name = '{technical}.test'
            _description = 'Simple model for {technical}'

            name = fields.Char(string='Name', required=True)
        """)

    def _render_views(self, technical, human_name):
        return textwrap.dedent(f"""\
        <?xml version="1.0" encoding="utf-8"?>
        <odoo>
            <record id="view_{technical}_form" model="ir.ui.view">
                <field name="name">{technical}.form</field>
                <field name="model">{technical}.test</field>
                <field name="arch" type="xml">
                    <form string="{human_name}">
                        <sheet>
                            <group>
                                <field name="name"/>
                            </group>
                        </sheet>
                    </form>
                </field>
            </record>

            <record id="view_{technical}_tree" model="ir.ui.view">
                <field name="name">{technical}.tree</field>
                <field name="model">{technical}.test</field>
                <field name="arch" type="xml">
                    <tree>
                        <field name="name"/>
                    </tree>
                </field>
            </record>

            <record id="action_{technical}_test" model="ir.actions.act_window">
                <field name="name">{human_name}</field>
                <field name="res_model">{technical}.test</field>
                <field name="view_mode">tree,form</field>
            </record>

            <menuitem id="menu_{technical}_root" name="{human_name}" sequence="10"/>
            <menuitem id="menu_{technical}_sub" name="Entries" parent="menu_{technical}_root" action="action_{technical}_test"/>
        </odoo>
        """)

    def _render_security_xml(self):
        return textwrap.dedent("""\
        <?xml version="1.0" encoding="utf-8"?>
        <odoo>
            <data noupdate="1">
                <record id="group_app_creator_user" model="res.groups">
                    <field name="name">App Creator User</field>
                    <field name="comment">Users who can create modules</field>
                </record>
            </data>
        </odoo>
        """)

    def _render_access_csv(self, technical):
        return f"id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\naccess_{technical}_test,access_{technical}_test,model_{technical}_test,base.group_user,1,1,1,1\n"

    def action_generate_module(self):
        """
        Called from the form button. This method is heavily logged to trace execution.
        """
        self.ensure_one()
        try:
            _logger.info("app_creator: action_generate_module START for technical_name=%s", self.technical_name)
        except Exception:
            pass

        # Test 1: confirm method entered
        try:
            _logger.info("app_creator: TEST 1 - button triggered")
        except Exception:
            pass

        # Validate technical name
        if not self.technical_name or not self.technical_name.strip():
            _logger.error("app_creator: TEST 2 - technical_name missing")
            raise UserError(_("Technical Name is required."))

        # Test 2: check BASE_PATH presence
        try:
            _logger.info("app_creator: TEST 3 - checking base path: %s", BASE_PATH)
            if not os.path.exists(BASE_PATH):
                _logger.error("app_creator: TEST 3 FAILED - base path not found: %s", BASE_PATH)
                raise UserError(_("Target directory %s not found.") % BASE_PATH)
            _logger.info("app_creator: TEST 3 OK - base path exists")
        except UserError:
            raise
        except Exception as e:
            _logger.error("app_creator: TEST 3 ERROR - %s", e)
            raise UserError(_("Error checking base path: %s") % e)

        # Module directory
        module_dir = os.path.join(BASE_PATH, self.technical_name)
        _logger.info("app_creator: TEST 4 - module_dir=%s", module_dir)

        if os.path.exists(module_dir):
            _logger.error("app_creator: TEST 4 FAILED - module already exists: %s", module_dir)
            raise UserError(_("Module directory '%s' already exists.") % module_dir)

        # Try to create directories
        try:
            _logger.info("app_creator: TEST 5 - creating module directories")
            os.makedirs(os.path.join(module_dir, "models"))
            os.makedirs(os.path.join(module_dir, "views"))
            os.makedirs(os.path.join(module_dir, "security"))
            _logger.info("app_creator: TEST 5 OK - directories created")
        except Exception as e:
            _logger.error("app_creator: TEST 5 FAILED - cannot create directories: %s", e)
            # cleanup partial creation if any
            try:
                if os.path.exists(module_dir):
                    _logger.info("app_creator: TEST 5 cleanup - removing partial module_dir")
                    # careful: only remove empty created dirs or try best-effort
                    for root, dirs, files in os.walk(module_dir, topdown=False):
                        for name in files:
                            try:
                                os.remove(os.path.join(root, name))
                            except Exception:
                                pass
                        for name in dirs:
                            try:
                                os.rmdir(os.path.join(root, name))
                            except Exception:
                                pass
                    try:
                        os.rmdir(module_dir)
                    except Exception:
                        pass
            except Exception:
                pass
            raise UserError(_("Failed to create module directories: %s") % e)

        # Write files step by step with logging
        try:
            _logger.info("app_creator: TEST 6 - writing __manifest__.py")
            manifest_path = os.path.join(module_dir, "__manifest__.py")
            _safe_write_file(manifest_path, self._render_manifest({
                'name': self.name,
                'version': self.version,
                'description': self.description or "",
                'author': self.author,
                'technical_name': self.technical_name,
            }))

            _logger.info("app_creator: TEST 7 - writing __init__.py")
            _safe_write_file(os.path.join(module_dir, "__init__.py"), self._render_init_py())

            _logger.info("app_creator: TEST 8 - writing models/__init__.py and models/models.py")
            _safe_write_file(os.path.join(module_dir, "models", "__init__.py"), self._render_models_init())
            _safe_write_file(os.path.join(module_dir, "models", "models.py"), self._render_models_py(self.technical_name))

            _logger.info("app_creator: TEST 9 - writing views")
            _safe_write_file(os.path.join(module_dir, "views", f"{self.technical_name}_views.xml"), self._render_views(self.technical_name, self.name))

            _logger.info("app_creator: TEST 10 - writing security")
            _safe_write_file(os.path.join(module_dir, "security", "security.xml"), self._render_security_xml())
            _safe_write_file(os.path.join(module_dir, "security", "ir.model.access.csv"), self._render_access_csv(self.technical_name))

            _logger.info("app_creator: TEST 11 - all files written")
        except UserError:
            raise
        except Exception as e:
            _logger.error("app_creator: TEST 11 FAILED - error writing files: %s", e)
            _logger.error("app_creator: TRACEBACK: %s", traceback.format_exc())
            # attempt cleanup
            try:
                if os.path.exists(module_dir):
                    _logger.info("app_creator: TEST 11 cleanup - removing created module_dir due to failure")
                    for root, dirs, files in os.walk(module_dir, topdown=False):
                        for name in files:
                            try:
                                os.remove(os.path.join(root, name))
                            except Exception:
                                pass
                        for name in dirs:
                            try:
                                os.rmdir(os.path.join(root, name))
                            except Exception:
                                pass
                    try:
                        os.rmdir(module_dir)
                    except Exception:
                        pass
            except Exception:
                pass
            raise UserError(_("Failed to write module files: %s") % e)

        # Finalize
        self.created_path = module_dir
        _logger.info("app_creator: TEST 12 - generation SUCCESS. Module created at: %s", module_dir)

        # Return a simple action to refresh form
        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }
