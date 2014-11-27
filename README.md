# The private Geoffrey UI repo

**Note**: has the normal geoffrey in a sub-repo but runs from over here

## Install:

    1. clone with submodules:
        git clone --depth=2 --recursive XXX
    2. virtualenv with geoffrey:

        virtualenv -p python2.7 .
        source bin/activate
        pip install -r requirements.txt

    3. Start celery:

    	python tasks.py

    4. Use:

        bin/twistd -n web --class main.API_SERVER
        bin/twistd -n web --class ui.WEB_UI

   
## Running

everything goes from here!

