from pynput import keyboard
from pynput import mouse
from pynput.mouse import Button, Controller
from queue import Queue

mapping = {}
curr_xy = Queue()

def read_mappings_as_list():
    mappings_str = ""
    with open('mappings.k2t', mode = 'r', encoding='utf-8') as file:
        mappings_str = file.read()

    mappings_list = mappings_str.split("mapping:")
    mappings_list = [mapping.replace("\n   "," ") for mapping in mappings_list]
    mappings_list = [mapping.replace("\n","") for mapping in mappings_list]
    mappings_list = [mapping.replace(" name:","name:") for mapping in mappings_list]
    mappings_list.remove('')
    mappings_list = [mapping.split(" keys:     ") for mapping in mappings_list]
    mappings_list = [[mapping[0].replace("name: ",""), mapping[1]] for mapping in mappings_list]

    return mappings_list

def calibration_listener(x, y, button, pressed):
    m_controller = Controller()
    if button == mouse.Button.left:
        if(pressed):
            print(f"clicked on ({x},{y})")
            m_controller.position = (x,y)
            print(f"controller position then claims to be at {m_controller.position}")
            # return False # Returning False if you need to stop the program when Left clicked.
    else:
        print('{} at {}'.format('Pressed Right Click' if pressed else 'Released Right Click', (x, y)))


def dictionary_val_filler_listener(x, y, button, pressed):
    if button == mouse.Button.left:
        if(pressed):
            print(f"value set to ({x},{y})")
            curr_xy.put((x,y))
            return False # Returning False if you need to stop the program when Left clicked.
    else:
        print('{} at {}'.format('Pressed Right Click' if pressed else 'Released Right Click', (x, y)))

def dictionary_key_filler_listener(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
        mapping[k] = (0,0) # default mapping to (0,0), will be changed at a later step
        print(f"Added {k} to mapping")

    except:
        k = key.name  # other keys
    

def key_event_handler(key):
    m_controller = Controller()
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
        if (k in mapping):
            print(f"moving mouse to {mapping[k]}")
            m_controller.position = tuple(coord/1.251 for coord in mapping[k])
            m_controller.press(Button.left)
    except:
        k = key.name  # other keys
    
    m_controller.release(Button.left)


    # return False

def init_mapping():
    print("Press the keys you want to map clicks to (esc when done)")
    listener_key = keyboard.Listener(on_press=dictionary_key_filler_listener)
    listener_key.start()  # start to listen on a separate thread
    listener_key.join()  # remove if main thread is polling self.keys
    listener_key.stop()

def fill_mapping():  
    for key in mapping:
        print(f"Click the spot on the screen for mapping for {key}")
        listener = mouse.Listener(on_click=dictionary_val_filler_listener)
        listener.start()  # start to listen on a separate thread
        listener.join()
        listener.stop()
        mapping[key] = curr_xy.get()

def save_mapping(name, dict):
    mapping_name = f"   name: {name}"
    new_mapping = "\n".join(["mapping:", mapping_name, "   keys: "])
    for key, val in dict.items():
        new_mapping = "\n".join([new_mapping, f"      {key}:{val}"])
    new_mapping += "\n\n"

    with open('mappings.k2t', mode = 'a', encoding='utf-8') as file:
        file.write(new_mapping)

def calibrate_click():
    listener = mouse.Listener(on_click=calibration_listener)
    listener.start()
    listener.join()

def read_mapping(name:str):
    mappings_list = read_mappings_as_list()
    i = 0
    wanted = -1
    for mapping in mappings_list:
        if mapping[0] == name:
            wanted = i
        i += 1
    if (wanted == -1):
        print(f"No mappings with the name {name} name found")
        return {}

    mapped_keys = mappings_list[wanted][1].split("    ")
    mapped_keys = [mapping.split(":") for mapping in mapped_keys]
    mapped_keys= [[mapping[0], mapping[1].replace("(", "")] for mapping in mapped_keys]
    mapped_keys= [[mapping[0], mapping[1].replace(")", "")] for mapping in mapped_keys]
    print(mapped_keys)


def main():
    changelog_str = ""
    version = "V#"
    with open('changelog.txt', mode = 'r', encoding='utf-8') as file:
        changelog_str = file.read()
    
    i = 1
    while(version[-2] != '\n'):
        # print(f"version[-2]: {version[-2]} -- changelog[i] = {changelog_str[i]}")
        version = version.replace('#', f"{changelog_str[i]}#") #honestly there's probably a better way to do this :v
        i += 1

    print(f"Welcome to key2touch {version[0:-2]}-")
    print("Changelog: ")
    print(changelog_str[i:], end="\n\n")

    if(version == "V0.0.1\n#"): # version 0.0.1 sucks ass, so if we're in V0.0.1 we tell the user to suck it
         print("Version 0.0.1 doesn't support any functionality at all. Please update key2touch.")
         return 0

    print("Hello! Welcome to k2t")
    print("Would you like to use an existing mapping or make a new one? e/n")
    response = input()
    if(response == "n"):
        print("What would you like to name the mapping (for the moment, please take care to not repeat, as the program cannnot yet check)")
        name = input()
        init_mapping()
        fill_mapping()
        save_mapping(name, mapping)
    if(response == "calibrate"):
        calibrate_click()
    else:
        print("No existing mappings exist (functionality not yet added) Bye")
        read_mapping("m1")
    
    print(f"Mapping : {mapping}")

    print("Entering map mode, press [esc] to exit")
    listener_key = keyboard.Listener(on_press=key_event_handler)
    listener_key.start()  # start to listen on a separate thread
    listener_key.join()  # remove if main thread is polling self.keys
    listener_key.stop()




if __name__ == "__main__":
    main()

# At the moment, when I click somewhere, if I try moving there, it will actually move to a position that's 1.25 times the place I clicked
    # That is to say, if I tell it to go to (0,0), it'll go to (0,0)
    # if I tell it to go to (400, 0), it'll go to (500,0)
    # if I tell it to go to (0, 400), it'll go to (0, 500)
    # and if I tell it to go to (400, 400), it'll go to (500, 500)
    # I don't know why this happens, but it does so I have to find a way to mitigate it. Should be easy

## k2t testing ##
# For the time being, k2t is more like k2m (key2mouseclick)

    # input 1 test line 21111111111111111
    # input 2 test line 233333433343334331144
    # input 3 test line 43442214444442441232
    # input 4 test line1 11414142221113