# massive-git-clone

This is a Python script that can be used to clone several Git repositories defined, via URL, into a text file.

## Help

```
$ ./massive-git-clone.py --help
usage: massive-git-clone.py [-h] -i INPUT -o OUTPUT [-a AUTH] [-v]

This is a Python script that can be used to clone several Git repositories defined, via URL, into a text file. - 2.0 (2025-02-26)

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file with the Git repositories URLs.
  -o OUTPUT, --output OUTPUT
                        Output folder where the repositories will be cloned.
  -a AUTH, --auth AUTH  Will ask for username and password to clone private repositories.
  -v, --verbose         Verbose mode
```

## Authors

* **Antonio Francesco Sardella** - *implementation* - [m3ssap0](https://github.com/m3ssap0)

## License

See the [LICENSE](LICENSE) file for details.