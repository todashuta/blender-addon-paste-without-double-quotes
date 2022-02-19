# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Paste without double quotes",
    "author": "todashuta",
    "version": (1, 0, 3),
    "blender": (2, 80, 0),
    "location": "File Browser",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "File Browser"
}


translation_dict = {
        "en_US": {
            ("Operator", "Paste without double quotes"): "Paste without double quotes",
        },
        "ja_JP": {
            ("Operator", "Paste without double quotes"): '前後の二重引用符（"）を除いて貼り付け',
        },
}


import bpy
import os
from pathlib import Path


class PASTE_WITHOUT_DOUBLE_QUOTES_OT_main(bpy.types.Operator):
    bl_idname = "file.paste_without_double_quotes"
    bl_label = "Paste without double quotes"
    bl_description = "Paste without double quotes"

    @classmethod
    def poll(cls, context):
        if not isinstance(context.space_data, bpy.types.SpaceFileBrowser):
            return False
        try:
            identifier = context.button_prop.identifier
            return identifier in {"directory", "filename"}
        except:
            return False

    def execute(self, context):
        s = context.window_manager.clipboard
        if s == "":
            print("[Paste without double quotes] empty string")
            return {"CANCELLED"}
        if s.startswith('"') and s.endswith('"'):
            s = s.strip('"')

        p = Path(s)
        try:
            if not p.exists():
                self.report({"WARNING"}, "File path is not valid.")
                return {"CANCELLED"}
        except:
            self.report({"ERROR"}, "File path is not valid.")
            return {"CANCELLED"}

        if p.is_file():
            filename = p.name
            directory = p.parent.resolve()
        else:
            filename = ""
            directory = p.resolve()

        context.space_data.params.filename = filename
        context.space_data.params.directory = bytes(str(directory), "UTF-8")
        return {"FINISHED"}


# This class has to be exactly named like that to insert an entry in the right click menu
class WM_MT_button_context(bpy.types.Menu):
    bl_label = "Unused"

    def draw(self, context):
        pass


def menu_func(self, context):
    if not PASTE_WITHOUT_DOUBLE_QUOTES_OT_main.poll(context):
        return
    layout = self.layout
    layout.separator()
    layout.operator(PASTE_WITHOUT_DOUBLE_QUOTES_OT_main.bl_idname)


classes = [
        PASTE_WITHOUT_DOUBLE_QUOTES_OT_main,
        WM_MT_button_context,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WM_MT_button_context.append(menu_func)

    bpy.app.translations.register(__name__, translation_dict)


def unregister():
    bpy.app.translations.unregister(__name__)

    bpy.types.WM_MT_button_context.remove(menu_func)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
