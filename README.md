# gCLIst

gCLIst is a simple Gist uploader. It's designed only for create a Gist and upload file(s). It is not for maintaining furthermore. If you need to edit the files, then you should use Git to clone the Gist, instead.

## Usage

    usage: gclist.py [-h] [-a] [-d DESCRIPTION] [-p] [-c SECTION]
                     [FILE [FILE ...]]

    Upload files to Gist.

    positional arguments:
      FILE                  File to upload (default: None)

    optional arguments:
      -h, --help            show this help message and exit
      -a, --anonymous       Upload anonymously (default: False)
      -d DESCRIPTION, --description DESCRIPTION
                            Description for Gist (default: None)
      -p, --private         Set Gist to private (default: False)
      -c SECTION, --config SECTION
                            Which INI section to use (default: default)

## Configuration

gCLIst looks for `gclistrc` in current directory or `~/$XDG_CONFIG_DIR/gclist/config` for configuration. Currently, it's only used for username and password. A sample configuration file looks like:

    [default]
    username = your_username
    password = your_password

    [other]
    username = other_username
    password = other_password

`[default]` is the default account. You can use `-c other` to use `[other]` in the case above.

## Examples

    $ ./gclist.py file1 file2

    $ ./gclist.py -

    $ ./gclist.py file1 - < file2

    $ cat file1 | ./gclist.py file2

If you use pipe or redirection, you will be asked for a filename.

## Output Example

    $ ./gclist.py *
    Uploading... done

    Gist 1179959 was created at
      https://gist.github.com/1179959
      git://gist.github.com/1179959.git

    User       : livibetter
    Public     : True
    Description: None

    Files:
        <script src="https://gist.github.com/1179959.js"> </script>

      gclist.py
        https://gist.github.com/raw/1179959/629cd5724db588b94f6f310199e966c94dc0a538/gclist.py
        <script src="https://gist.github.com/1179959?file=gclist.py"></script>

      README.md
        https://gist.github.com/raw/1179959/399ed4784548953b5b62bf21d19121c293dd6de0/README.md
        <script src="https://gist.github.com/1179959?file=README.md"></script>

## Notes

Although I intend to make gCLIst only for uploading once, then editing using Git. But if you want to make it a super CLI command, feel free to add pull requests. I would be glad to include your enhancements.
