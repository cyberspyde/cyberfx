Script to rename all the files inside the current folder which has spaces to underscores recursively.
```bash
find . -depth -name '* *' -exec bash -c 'mv -v "$1" "${1// /_}"' _ {} \;
```