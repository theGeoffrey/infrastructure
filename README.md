# The private Geoffrey UI repo

**Note**: has the normal geoffrey in a sub-repo but runs from over here

## Install:

    1. clone with submodules:
        git clone --depth=2 --recursive XXX
    2. virtualenv with geoffrey:

        virtualenv -p python2.7 .
        source bin/activate
        pip install -r requirements.txt

    3. profit!

        bin/twistd -n web --class main.API_SERVER

## Running

everything goes from here!

