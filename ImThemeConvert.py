import re

def rgba_to_imgui_color(rgba_str):
    rgba = [float(x) for x in re.findall(r"[\d.]+", rgba_str)]
    return f"ImVec4({round(rgba[0]/255, 6)}, {round(rgba[1]/255, 6)}, {round(rgba[2]/255, 6)}, {round(rgba[3], 6)})"


def toml_to_imgui_style(toml_str):
    toml_lines = toml_str.split("\n")

    imgui_style = []
    inside_colors = False

    for line in toml_lines:
        if line.startswith("[themes.style]"):
            continue
        elif line.startswith("[themes.style.colors]"):
            inside_colors = True
            continue
        
        if inside_colors:
            if "=" in line:
                key, value = line.split("=")
                key = key.strip().replace(" ", "")
                value = rgba_to_imgui_color(value.strip())
                imgui_style.append(f"style.Colors[ImGuiCol_{key}] = {value};")
        else:
            if "=" in line:
                key, value = line.split("=")
                key = key.strip()
                key = key[0].upper() + key[1:]
                value = value.strip()
                if "[" in value:
                    value = value.replace("[", "ImVec2(").replace("]", ")")
                elif "None" in value:
                    value = "ImGuiDir_None"
                elif "Right" in value:
                    value = "ImGuiDir_Right"
                elif "Left" in value:
                    value = "ImGuiDir_Left"
                imgui_style.append(f"style.{key} = {value};")

    return "\n".join(imgui_style)

toml_str = """
# The given TOML-style theme should be placed here

"""

cpp_imgui_style = toml_to_imgui_style(toml_str)
print(cpp_imgui_style)
