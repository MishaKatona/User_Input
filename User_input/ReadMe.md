# User Input Docs

## The UserInput Class
This class generates the input widget that can be added to any layout,
and contains the individual input frames with which values can be 
passed to the program.

**Initialisation:** UserInput needs to be initialised with at least 9 inputs with 2 further optional ones,
all of which are described in the class. Once initialised the widget can be retrieved with the **get_input_widget()** method,
the state and values of the generated widget can be set with the 
**set_values(values)**, and **set_state(state)** methods.

**Value Retrieval:** There are two ways to retrieve information from the input widget, 
first by passing a callback function with the interface of **callback(path: list, value)**. This function
gets called everytime there is a value change, and returns the dictionary keys in the
form of a path along with the new value. The other way is to call the **get_values()**
method, which has a complimentary method of **get_state()** both of which return 
dictionaries with the same shape as the input_definitions.

## Frame Template
There are 6 parts that compose up a frame, with every element having to be fully defined
or set to None. This however does not meant hat the final template must be fully defined,
as templates are merged from default -> type templates -> user defined frame. (With 
the possibility of more intermediate (re)definitions of templates possible)

#### Label
- **Alignment** - str - Set the alignment of the Label
  - "Left", "Center", "Right", "Fill"
- **Bold** - boolean - If the text should be Bold
- **Italic** - boolean - If the text should be Italic
- **MaxWidth**  - int - Maximum width of text, after which it wraps to next line
- **IconSize** - int - Size of the icons that can display in the label
- **Text** - str - (OPTIONAL in the user defined) Sets the displayed text for the Label
  (instead of the key)

#### InputItem
- **Type** - str - A key of an input item that is passed to UserInput -> input_element_templates
- **Location** - str - Sets the location of the input item
  - "Right", "Below"
- **Alignment** - str - Set the alignment of the input item
  - "Left", "Center", "Right", "Fill"
- **HideOnExpand** - boolean - If the body becomes visible hide the input item

#### Description
- **Text** - str - Text to display in the description
- **Hover** - boolean - If the description should be a tooltip or added to the frame
- **MaxWidth** - int - Sets the max width of the tooltip

#### Body
- **Widget** - str - A key of a body widget that is passed to UserInput -> body_dict_list
- **Args** -  - Any arguments that the widget uses at initialisation
- **Expanded** - boolean - Sets the initial expand state
- **AlwaysExpanded** - boolean - If the body should always be visible (Removes expand button)
- **ExpandOnValue** - boolean - Passes the value of the header input item as the expand state
- **Indent** - int - How much from the left should the body be indented

#### ExpandButton
- **Size** - int - Size of the expand button
- **Border** - boolean - If the expand button should have a border

#### Settings
- **Padding** - list - Sets the [left, top, right, bottom] padding of the frame
- **AllowLock** - boolean - If the lock_state can be set to true


# TODO

Add multiple grouping and tabbing categories

It might be nice to easily update the default template

Add depth detection

In textedit focus lost should remove cursor

Niche issue if the parent key in definitions same as a definition key,
this can crash the program in trying to group by level.
example {"key1": {"key1": {definition}} -> can crash
if grouping by 0 (In cases where the tab and
group are the same key or something). This probaby 
tries to add_frame itself recursively

Add warnings for incorrect grouping
