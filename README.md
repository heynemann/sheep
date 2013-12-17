sheep
=====

sheep is a `dead-simple` worker process manager.

<blockquote>Contrary to what you may have heard or even expressed yourself, sheep are not stupid. (<a href="http://www.livestocktrail.illinois.edu/sheepnet/paperDisplay.cfm?ContentID=1">An Introduction to Sheep Behavior - Richard Cobb</a>).</blockquote>

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

How to add my own configuration keys?
-------------------------------------

Since sheep uses [derpconf](https://github.com/globocom/derpconf), all you need to do is create a file with the configuration keys for your application. We'll call this file `my_worker.conf` for this example:

```python
# the configuration names MUST be in uppercase,
# otherwise derpconf will ignore them
CONFIG1 = "test"
CONFIG2 = "other"
```

When invoking your `Shepherd`, just use the `--config` option:

    $ python my_worker.py --config=./my_worker.conf

Then in your `Shepherd` those become available via the `config` property:

```python
from sheep import Shepherd

class MyWorker(Shepherd):
    def do_work(self):
        # do some heavy work
        print(self.config.CONFIG1)  # prints "test"
        print(self.config.CONFIG2)  # prints "other"

if __name__ == "__main__":
    MyWorker.run()
```

How to add default values for configuration keys?
-------------------------------------------------

Subclassing [derpconf's](https://github.com/globocom/derpconf) `Config` class you can specify defaults for your keys. Just create a `config.py` file with something like this:

```python
from derpconf.config import Config

Config.define('foo', 'fooval', 'Foo is always a foo', 'FooValues')
```

Now, all that you need to do is tell your `Shepherd` where he can find your `Config` class:

```python
from sheep import Shepherd
from config import Config

class MyWorker(Shepherd):
    def get_config_class(self):
        return Config  # just return the class type and
                       # Shepherd will take care of the rest

    def do_work(self):
        # do some heavy work
        print(self.config.foo)  # prints "fooval" even if no config 
                                # file specified or key not found in 
                                # config file

if __name__ == "__main__":
    MyWorker.run()
```

How to initialize services?
---------------------------

Many times you'll need to initialize some service, like connecting to a database. Sheep got you covered. Just override the `initialize` method in your `Shepherd`:

```python
from sheep import Shepherd
from db import connect

class MyWorker(Shepherd):
    def initialize(self):
        self.db = connect(self.config.CONNECTION_STRING)

    def do_work(self):
        # do some heavy work
        self.db.execute('SELECT baz FROM foo')  # or something like it

if __name__ == "__main__":
    MyWorker.run()
```

Since `initialize` is called in the end of your `Shepherd's` constructor, the configuration keys will be available to you already.

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

How to add arguments?
---------------------

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

What if my worker raises an exception?
--------------------------------------

If your `do_work` method raises any exceptions, your `Shepherd` will log it to the standard output and run `do_work` again. Sheep won't let your worker die in the face of an exception.

"What if it gets a SEGFAULT error while doing its work?", you'll ask. Well, we are prepared for that. If the fork that's running your work dies, sheep will revive it and start running it again.

How can I handle the exceptions it raises?
------------------------------------------

Assuming it's a trappable error (not a SEGFAULT), you can use the `handle_error` method in your `Shepherd` class to do something with the error, like logging it to an error collector like `Sentry`.

```python
from sheep import Shepherd

class MyWorker(Shepherd):
    def handle_error(self, exc_type, exc_value, tb):
        # do something with the exception information
        pass

    def do_work(self):
        # do some heavy work
        raise RuntimeError('woot?')

if __name__ == "__main__":
    MyWorker.run()
```

How to Contribute
-----------------

Fork, branch, pull request. Same ol', same ol'.

License
-------

Look at the LICENSE file.
