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

get_description
---------------

You should override this method in your Shepherd in order to get better logging messages when running your worker.

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
