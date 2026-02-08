# -*- coding: utf-8 -*-
{
    "name": "App Creator",
    "version": "1.0.0",
    "summary": "Generate new Odoo modules automatically (instrumented)",
    "description": "Generates modules inside D:\\odoo18 for\\odoo\\addons_apps and logs each step for debugging.",
    "author": "Aymen Barkat (instrumented)",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": ["base"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/app_creator_views.xml",
    ],
    "installable": True,
    "application": True,
}
