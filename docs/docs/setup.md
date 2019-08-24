
In here we're going to install, init and serve our **Mocha** application

---

## Install

The best way to install **Mocha** is to do it with pip.

    pip install mocha

It's preferable to install your Mocha app into it's own virtual environment.

---

## Init

Once installed, use the command line `mocha` to initiate the application.

Make sure that you `cd` into the right directory to run the command, as it will place the data in the current working dir.

So run:

    mocha :init

It will create all the necessary files to get going, and you should see a file structure similar to the one below

{!_partials/file-structure.md!}

---

## Serve

Now your Mocha app is ready to go, it's time to serve it.

    mocha :serve

You can access by default the application at: `http://localhost:5000`

To serve on a different port:

    mocha :serve --port 5001

-> `http://localhost:5001`

---
