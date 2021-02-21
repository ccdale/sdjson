# ccasdtv project

Currently in development.

## Install
```
# install dependencies
poetry install
# create a config file
touch ~/.config/ccasdtv.yaml
# Run the app with
poetry run python sdjson/sd.py
```

## Status
currently will obtain a SD API token and cache it for 23 hours in the config
file, along with your sha1 hashed password.

## Data Cache
All channel and program data will be cached on disk.

Channel data will be organised by channel and then by date in seperate
directories.

Individual program data will be organised by the first 4 characters of the
md5 hash of the program, making each one simple to find.
```
.ccasdtv |
        channel |
                BBC1 |
                    <date>
                    <date>
                    ...
                    <date>
                BBC2 |
                    <date>
                    <date>
                    ...
                    <date>
                ...
                BBC4 |
                    <date>
                    <date>
                    ...
                    <date>
        programs |
            a |
                ab |
                    abc |
                        abcd |
                            abcd<md5>.json
                            abcd<md5>.json
                            ...
                            abcd<md5>.json
                        abce |
                            abce<md5>.json
                            abce<md5>.json
                            ...
                            abce<md5>.json
                        ...
                        zzzz |
                            zzzz<md5>.json
                            zzzz<md5>.json
                            ...
                            zzzz<md5>.json
