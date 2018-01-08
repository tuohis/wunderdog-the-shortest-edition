# Wunderdog - The Shortest Edition #

This is a silly exercise where a text has to be fitted onto 80-character lines by rearranging the words.

The program prints the new and improved version of the text to stdout.

## Requirements ##

- A standard Python3 environment

## Running ##

Usage: `python3 main.py [-h] [--test] [source_file]`

Parameters:

- `-h` - print the help message
- `--test` - run in test mode: print only statistics instead of the actual output
- `source_file` - the file containing the input text; if omitted, the input data will be downloaded over the Internet

### Examples ###

Use a local file as the source file and print to stdout:

`python3 main.py alastalon_salissa.txt`

Use a local file as the source file and save the output to file:

`python3 main.py alastalon_salissa.txt > result.txt`

Let the program to download the source file and print to stdout:

`python3 main.py`

You can also run it as a script in a bash-like shell with the same parameters as above:

```
chmod 755 main.py
./main.py [-h] [--test] [source_file]
```

## Copyright and License ##

Author and copyright holder: Mikko Tuohimaa (mikko.tuohimaa@iki.fi). The program is licensed under the MIT license.
