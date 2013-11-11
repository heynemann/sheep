sheep
=====

sheep is a `dead-simple` worker process manager.

Why?
----

Writing worker processes that do background processing is a fairly common task.

At the time sheep was created there was no available solution to the requirements.

Requirements
------------

sheep must be able to:

* Easy to use configuration (sheep uses [derpconf](https://github.com/globocom/derpconf));
* Easy to fork (spawning multiple workers with a single command);
* Reliability when running an unit-of-work (must not die even in the face of SEGFAULT);
* Ease-of-use (Implementing a new worker must be really simple).

Without further ado, let's see how to implement and use sheep.

Installing
----------

Installing is as easy as:

    $ pip install sheep

The Shepherd
------------

The class required to run sheep is the `Shepherd`. All you need to do is subclass it like this:

```python
from sheep import Shepherd

class MyWorker(Shepherd):
    def do_work(self):
        # do some heavy work
        print("Done")

if __name__ == "__main__":
    MyWorker.run()
```

Save this in a file called `my_worker.py`. Then running your new worker is as easy as:

    $ python my_worker.py

You can see all the options with `--help`:

    $ python my_worker.py --help

How to change my worker's name?
------------------------------

You should override the `get_description` method in your `Shepherd` in order to get better logging messages when running your worker.

Just return whatever text you want to be used as the name of your parent worker.

```python
from sheep import Shepherd

class MyWorker(Shepherd):
    def get_description(self):
      return "My Funky Worker v1.0.0"

    def do_work(self):
        # do some heavy work
        print("Done")

if __name__ == "__main__":
    MyWorker.run()
```

How to add arguments
--------------------

As with the arguments you can already pass to your `Shepherd`, you can add more of your own. Just override the `config_parser` method:

```python
from sheep import Shepherd

class MyWorker(Shepherd):
    def config_parser(self, parser):
      # parser is an instance of argparse.ArgumentParser
      # just use the regular argparse configuration methods
      parser.add_argument('--foo', help='foo help')

    def do_work(self):
        # do some heavy work
        print("Done")

if __name__ == "__main__":
    MyWorker.run()
```

Now `my_worker.py` can be called with `--foo`:

    $ python my_worker.py --foo
