PYTHON=`which python3.3`

build: deps statics

statics: venv
	venv/bin/python manage.py collectstatic --noinput

deps: venv
	venv/bin/pip install -r requirements.txt

venv:
	virtualenv venv --python ${PYTHON}

clean:
	rm -rf venv
	rm -rf public
