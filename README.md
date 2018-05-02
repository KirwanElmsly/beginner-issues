# beginner-issues

Under Development & Incomplete.

Web application to aggregate GitHub issue search results for multiple labels.

So I couldn't figure out how to include multiple labels while searching GitHub issues so I quickly wrote up a Python script to aggregate results for multiple labels. Currently making it work as a simple web app with a Flask back end. I haven't really done much web development in the past so this is a learning process for me. This might take a while too as I don't have much time to work on it.

Feedback is appreciated! Feel free to message me with feedback or if you think this is stupid.

## Getting Started

### Prerequisites

* Python 3.6
* Pip
* VirtualEnv (Optional but recommended)

### Installing

First, clone this repository.
```
$ git clone https://github.com/KirwanElmsly/beginner-issues
$ cd beginner-issues
```

Create a virtualenv, and activate:
```
$ virtualenv env
$ source venv/bin/activate
```

Install all necessary dependencies:
```
$ pip install -r requirements.txt
```

Run the application:
```
$ python run.py
```

To see your application, go to this url in your browser:
```
http://127.0.0.1:5000
```


All configuration is in: `config.py`

## Testing

No tests as of yet.

## Built With

* [Flask](http://flask.pocoo.org/) - web framework

## Authors

* **Kirwan Elmsly**
