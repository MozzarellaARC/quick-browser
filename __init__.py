# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy

addon_keymaps = []


def toggle_asset_browser_split():
    screen = bpy.context.screen
    asset_area = next(
        (a for a in screen.areas if a.type == "FILE_BROWSER" and a.ui_type == "ASSETS"),
        None,
    )

    if asset_area:
        with bpy.context.temp_override(area=asset_area):
            bpy.ops.screen.area_close()
        return

    view3d_area = next((a for a in screen.areas if a.type == "VIEW_3D"), None)
    if not view3d_area:
        return

    region = next((r for r in view3d_area.regions if r.type == "WINDOW"), None)
    if not region:
        return

    with bpy.context.temp_override(area=view3d_area, region=region):
        bpy.ops.screen.area_split(direction="VERTICAL", factor=0.5)

    new_area = screen.areas[-1]
    new_area.type = "FILE_BROWSER"
    new_area.ui_type = "ASSETS"


class QuickAssetBrowser_Operator(bpy.types.Operator):
    bl_idname = "wm.quick_asset_browser"
    bl_label = "Toggle Asset Browser"
    bl_description = "Toggle the Asset Browser panel"

    def execute(self, context):
        toggle_asset_browser_split()
        return {"FINISHED"}


class CloseConsole_Operator(bpy.types.Operator):
    bl_idname = "wm.close_console_terminal"
    bl_label = "Close Console Terminal"
    bl_description = "Close the console/terminal panel if active"

    def execute(self, context):
        area = context.area
        if area and area.type == "CONSOLE":
            with context.temp_override(area=area):
                bpy.ops.screen.area_close()
        return {"FINISHED"}


class QuickAssetBrowser_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        layout.label(text="No preferences available.")


def register():
    bpy.utils.register_class(QuickAssetBrowser_Operator)
    bpy.utils.register_class(QuickAssetBrowser_Preferences)
    bpy.utils.register_class(CloseConsole_Operator)

    # Add keymaps
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        # Console context keybind
        km = kc.keymaps.new(name="Console", space_type="CONSOLE")
        kmi = km.keymap_items.new(
            CloseConsole_Operator.bl_idname, "ACCENT_GRAVE", "PRESS"
        )
        addon_keymaps.append((km, kmi))


def unregister():
    # Remove keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(CloseConsole_Operator)
    bpy.utils.unregister_class(QuickAssetBrowser_Operator)
    bpy.utils.unregister_class(QuickAssetBrowser_Preferences)
