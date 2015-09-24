# HTTP log monitoring console program

[ ![Codeship Status for MickaelBergem/test-datadog](https://codeship.com/projects/db2f8a20-90df-0132-649c-76ae55305aa6/status?branch=master)](https://codeship.com/projects/61603)

## Usage

    python3 monitoring.py /var/log/apache2/access.log

You can generate fake log entries to test the program with `demologfeeder.py` :

    python3 demologfeeder.py -d 0.01 /tmp/demo.log

![Demo](demo.png)

## Testing

### Installing coverage and py.test

    virtualenv venv --python=python3
    source venv/bin/activate
    pip install -r requirements.txt

### Running the tests

    coverage run --source='.' -m py.test tests

To read the coverage report :

    coverage report -m
