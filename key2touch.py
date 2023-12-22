from pynput import keyboard
from pynput import mouse
from pynput.mouse import Button, Controller
from queue import Queue

# mapping = {}
mapping_q = Queue()
curr_xy = Queue()

'''
========= FUNCTION: read_mappings_as_array =========
Args: none
Returns: a python array which contains all mappings as an array of the form: 
            [name, [mappings]]
'''
def read_mappings_as_array(): 
    # First we open the file as a string
    mappings_str = ""
    with open('mappings.k2t', mode = 'r', encoding='utf-8') as file:
        mappings_str = file.read()

    mappings_list = mappings_str.split("mapping:") # we split it based on what we have before each mapping
    mappings_list = [mapping.replace("\n   "," ") for mapping in mappings_list] # remove all the \n's with a buncha spaces after them 
    mappings_list = [mapping.replace("\n","") for mapping in mappings_list] # remove all remaining \n's
    mappings_list = [mapping.replace(" name:","name:") for mapping in mappings_list] # we do some quick reformatting on the "name" department
    mappings_list.remove('') # There's an empty item at the beginning of the list, we don't want that
    mappings_list = [mapping.split(" keys:     ") for mapping in mappings_list] # Now we split each item into [name, keys]
    mappings_list = [[mapping[0].replace("name: ",""), mapping[1]] for mapping in mappings_list] # and finally, we remove the part that says "name"

    return mappings_list

'''
========= FUNCTION: calibration_listener =========
args: 
    - x: the x position of the mouse
    - y: the y position of the mouse
    - button: what mouse button is being pressed
    - pressed: whether the button `button` is being pressed or released
returns: none

This function is a mouse listener that I used when debugging the mouse issue mentioned to exist in
V0.0.2 as per the changelog. the listener will wait for a click, register where the click was, then
move the mouse to that position. Since this is a debug function made for me, it won't get properly
documented.
'''
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

'''
========= FUNCTION: dictionary_val_filler_listener =========
args: 
    - x: the x position of the mouse
    - y: the y position of the mouse
    - button: what mouse button is being pressed
    - pressed: whether the button `button` is being pressed or released
returns: none

This is a listener that will take the position of a click and save it as an item in the queue called
curr_xy
'''
def dictionary_val_filler_listener(x, y, button, pressed):
    if button == mouse.Button.left:
        if(pressed): # if the left click is being pressed
            print(f"value set to ({x},{y})") 
            curr_xy.put((x,y)) # save the value where the mouse was to the queue
            return False # Returning False so that the function will only really end if you press, not when you release. If you release, nothing happens
    else:
        print('{} at {}'.format('Pressed Right Click' if pressed else 'Released Right Click', (x, y)))

'''
========= FUNCTION: disctionary_key_filler_listener =========
args: 
    - key: Current key being pressed
returns: none

This function is a listener for the keyboard, upon receiving a key, it will add it as a key for the mapping
dictionary and default it to (0,0). then it takes this mapping and saves it to a queue called mapping_q
'''
def dictionary_key_filler_listener(key):
    mapping = {}
    if(not mapping_q.empty()):
        mapping = mapping_q.get() # making a dict called "mapping" which initialized to whatever's in queue (starts empty)
    # print("mapping it being reset lol loser fuck you")
    if key == keyboard.Key.esc: # the esc key quits. Cannot be enter because that kind of messes up the terminal after the program runs :/
        # print(f"mapping at the end of filler_listener: {mapping}")
        mapping_q.put(mapping) # before leaving, we save the mapping to the queue
        return False  # stop listener
    try:
        k = key.char  # single-char keys
        mapping[k] = (0,0) # default mapping to (0,0)
        print(f"Added {k} to mapping")
        mapping_q.put(mapping)

    except:
        k = key.name  # other keys
    
'''
========= FUNCTION: key_event_handler =========
args: 
    - key: Current key being pressed
returns: none

This function is a listener for the keyboard, upon receiving a key, it will check if the key is in the mapping,
which it will get from the queue. It also puts the mapping back into the queue because for some reason when 
you call "get" it removes the item from the queue. When it gets the mapping, it checks if the key that has just
been pressed is IN the mapping, and if it is, it will move the mouse to the place it wants to go and click the mouse
'''
def key_event_handler(key):
    mapping = mapping_q.get() # get the mapping
    mapping_q.put(mapping) # put the mapping back in queue, we can keep using the mapping variable anyhow
    m_controller = Controller() # make a mouse controller

    if key == keyboard.Key.esc: # esc is ALSO the key to leave here. this one does make sense though.
        return False  # stop listener
    try:
        k = key.char  # single-char keys
        if (k in mapping): # if K is in mapping (as a key)
            print(f"moving mouse to {mapping[k]}")
            m_controller.position = tuple(coord/1.25 for coord in mapping[k]) # we can move the controller position (to check why we divide, look at the changelog)
            m_controller.press(Button.left) # we can press the button
    except:
        k = key.name  # other keys
    
    m_controller.release(Button.left) # then we release it (this will have to be changed at a later version... we might need a listener to press and one to release)

'''
========= FUNCTION: init_mapping =========
args: none
returns: none

This function will initiate mapping. It just calls the key_filler_listener to fill the dictionary with all the 
defaults
'''
def init_mapping():
    print("Press the keys you want to map clicks to (esc when done)")
    listener_key = keyboard.Listener(on_press=dictionary_key_filler_listener)
    listener_key.start()  # Just start the listener
    listener_key.join()  # remove if main thread is polling self.keys
    listener_key.stop() # stop when done :)

'''
========= FUNCTION: fill_mapping =========
args: none
returns: none

This function is the function that will change the defaults in the mapping to the desired points in the screen.
It does this by getting the mapping from the queue, then starting the dictionary_val_filler listener, and then using
the stuff that one puts in ITS queue to change the mappings for the mapping dictionary
'''
def fill_mapping():
    mapping = mapping_q.get() # get mapping
    # print(f"mapping at the start of 'fill_mapping': {mapping}")
    for key in mapping: # for each key in the mapping dictionary
        print(f"Click the spot on the screen for mapping for {key}")
        listener = mouse.Listener(on_click=dictionary_val_filler_listener) # we can start the dictionary_val_filler_listener
        listener.start()  # start to listen on a separate thread
        listener.join()
        listener.stop()
        mapping[key] = curr_xy.get() # after the listener stops, we can check what value it put in the curr_xy queue
    # print(f"mapping at the end of 'fill_mapping': {mapping}")
    mapping_q.put(mapping) # after we're done modifying all of the mappings, we can put it all in the queue again (but it's the new mappings now)

'''
========= FUNCTION: save_mapping =========
args:
    - name: A string with the name you're saving the mapping as
    - dict: the dictionary with the mappings 
returns: none

This function takes the current mapping and saves it into the .k2t file
'''
def save_mapping(name:str, dict):
    name_new = name.split(" ")
    new_name = name_new[0] #If the user adds a space, ignore everything after the first space
    # print(f"Name chosen: {new_name}")
    mappings_list = read_mappings_as_array() # takes the current existing mappings as an array
    for m in mappings_list: # this loop checks if the desired name exist
        if new_name == m[0]: # and if DOES exist
            print(f"Mapping with name {new_name} already exists")
            i = 1
            for m2 in mappings_list: # we begin this loop, which will check if the mappings with the same name but with numbers
                if f"{new_name}_{i}" == m2[0]:
                    i += 1
            print(f"changing name to {new_name}_{i}...") # and then it changes the name of the new mapping
            new_name = f"{new_name}_{i}"
    
    # This section here will format the mapping in a standard way that can be decoded by the read_mappings_as_array function
    mapping_name = f"   name: {new_name}"
    new_mapping = "\n".join(["mapping:", mapping_name, "   keys: "])
    empty_keys = True
    for key, val in dict.items():
        empty_keys = False 
        new_mapping = "\n".join([new_mapping, f"      {key}:{val}"])
    if empty_keys: # if we have no keys (this shouldn't happen)   
        print("ERROR: NO KEYS FOUND IN MAPPING. ADDING DEFAULT KEY MAPPING 0:(0,0)")
        new_mapping = "\n".join([new_mapping, f"      0:(0,0)"]) # we invent one just so we don't die when reading the file later on
    new_mapping += "\n\n"

    # and then the new mapping gets written into the k2t file
    with open('mappings.k2t', mode = 'a', encoding='utf-8') as file:
        file.write(new_mapping)

'''
========= FUNCTION: calibrate_click =========
args: none
returns: none

This function calls the calibration_listener. More info on that in the calibration_listener function
'''
def calibrate_click():
    listener = mouse.Listener(on_click=calibration_listener)
    listener.start()
    listener.join()

'''
========= FUNCTION: read_mapping =========
args:
    - name: a string of the mapping you're tryna read
returns:
    - mapping: a dictionary with the read mapping

This function is the function reads a mapping from the .k2t file and returns it as a dictionary
'''
def read_mapping(name:str):
    mappings_list = read_mappings_as_array() # read the existing mappings
    i = 0 
    wanted = -1
    for mapping in mappings_list: # look for the desired mapping
        if mapping[0] == name: # if we find the mapping we want, we say that's it
            wanted = i
        i += 1
    if (wanted == -1): # if we didn't find a mapping
        print(f"No mappings with the name {name} name found")
        return {} # mapping is null fuck you :3

    mapped_keys = mappings_list[wanted][1].split("    ") # select the mapping we want and start turning the keys into a tuple of ints (idk why it's here that we do this ngl)
    mapped_keys = [mapping.split(":") for mapping in mapped_keys]
    mapped_keys= [[mapping[0], mapping[1].replace("(", "")] for mapping in mapped_keys]
    mapped_keys= [[mapping[0], mapping[1].replace(")", "")] for mapping in mapped_keys]
    mapped_keys= [[mapping[0], mapping[1].split(", ")] for mapping in mapped_keys]
    mapped_keys= [[mapping[0], tuple(int(number) for number in mapping[1])] for mapping in mapped_keys]
    # ^ everything up to here is just turning the second item of the mapping into a tuple of int
    new_mapping = {}
    for m in mapped_keys:
        new_mapping[m[0]] = m[1] # turn the list into a dictionary
    
    return new_mapping # return this dictionary

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

    print(f"Welcome to key2touch -- {version[0:-2]} --")
    print("Changelog: ")
    print(changelog_str[i:], end="\n\n")

    if(version == "V0.0.1\n#"): # version 0.0.1 sucks ass, so if we're in V0.0.1 we tell the user to suck it
         print("Version 0.0.1 doesn't support any functionality at all. Please update key2touch.")
         return 0

    print("Hello! Welcome to k2t")
    print("Would you like to use an existing mapping or make a new one? e/n")
    response = input()
    if(response == "n"):
        print("What would you like to name the mapping?")
        name = input()
        init_mapping()
        fill_mapping()
        try:
            mapping = mapping_q.get()
            mapping_q.put(mapping)
            save_mapping(name, mapping)
        except:
            print("No mapping created. Exiting")
            return  
    elif(response == "calibrate"):
        calibrate_click()
    else:
        # print("No existing mappings exist (functionality not yet added) Bye")
        print("What's the name of the mapping you're looking for?")
        load_mapping = input()
        mapping = read_mapping(load_mapping)
        mapping_q.put(mapping)
   
    mapping = mapping_q.get()
    mapping_q.put(mapping)
    print(f"Mapping : {mapping}")

    print("Entering map mode, press [esc] to exit")
    listener_key = keyboard.Listener(on_press=key_event_handler)
    listener_key.start()  # start to listen on a separate thread
    listener_key.join()  # remove if main thread is polling self.keys
    listener_key.stop()


if __name__ == "__main__":
    main()

## k2t testing ##
# For the time being, k2t is more like k2c (key2click)

    # input 1 test line 11112224332222222224212
    # input 2 test line 222221444443311133444144433334343443333334
    # input 3 test line 3333324144222244414411122442
    # input 4 test line 44444433122222322222211122211325113