# mkmenu

mkmenu converts simple text files to Openbox compatible XML. It is similar
to menumaker in purpose however this is openbox exclusive and aims to be *very* simple.

# Usage

Run `mkmenu -h`.

# Creating a Menu File

Menus are generated from plain text files, and they follow a very simple structure

```
#named separator
category
  item:cmd
  #named separator
  item:cmd
  ---
  subcategory
    item:cmd
    item:cmd
    item:cmd
item:cmd
item:cmd
```

- Where `---` is a separator, without any text.
- Identation (2 spaces) controls the scope of the menus.
- For commands to be run on a terminal emulator prepend `@T` before the command
- `@T` will be converted your terminal command of choice, by default `st -e` is used.
- You can have multiple files as input, they'll be concatenated in order of
  input as one file and then processed into XML.
