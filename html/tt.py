import json
def auto_connect():
    """通过读取config.json文件的wifi字段，自动连接wifi"""
    config_path = "templates/config.json"
    config_info = {}
    with open(config_path, "r", encoding="UTF-8") as file:
        config_info = json.load(file)
    return config_info

print(auto_connect())

gpio_info = {
    "1": "abc",
    "2": "dfg",
    "3": "3abc",
    "4": "4dfg"
}
gpio_button_element = "___gpio_namber\n" \
                      "---gpio_info\n" \
                      "___gpio_namber\n" \
                      "---gpio_info"
gpio_button = ""
for key, value in gpio_info.items():
    if "gpio_namber" in gpio_button:
        gpio_button = gpio_button.replace("gpio_namber", key, 1).replace("gpio_info", value, 1)
    else:
        gpio_button += gpio_button_element.replace("gpio_namber", key, 1).replace("gpio_info", value, 1)
        # gpio_button = gpio_button.replace("gpio_namber", key, 1).replace("gpio_info", value, 1)
print(gpio_button)
