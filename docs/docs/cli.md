Mocha provides a command line tool to do sim

    mocha

### :init

Running init will initialize mocha in the current directory

    mocha :init

---

### :serve

Run the server in the development mode.

    mocha :serve

By default it will run the `main` application in `config.Dev` environment

To change application and environment, prepend the app before mocha :serve

    app=main:production mocha :serve

The code above will run the `main` application with the `config.Production`

    app=admin:stage mocha :serve

The code above will run `admin` application with `config.Stage`

    env=production mocha :serve

The code above will run the `main` application with `config.Production`.

When `app` is not provided, or only `env` is provided, it will assume the app is `main`

---

### :addview

To create a new view

    mocha :addview

---

### :install-assets

To install assets from `application/assets/package.json`

This command requires `npm` as it will run `npm install` to install the assets

    mocha :install-assets

---

### :dbsync

To create new models in your DBMS.

    mocha :dbsync


---

### :assets2s3


When `config.ASSETS_DELIVERY_METHOD` is `S3`, this util will allow you to upload
your assets to S3, and the application will automatically point all your assets
to S3.

    mocha :assets2s3

Since it will be in production or some other places other than local,
you may need to add the environment variables

    app=main:production mocha :assets2s3


---

## Develop CLI

You can develop your own CLI to also attach to the `mocha` cli.

This will allow you to admin your application within one command line.

Mocha provides a CLI interface using `click`


### Create

    import mocha.cli
    class MyCLI(mocha.cli.CLI):

        def __init__(self, command, click):

            @command('hello-world')
            def hello_world():
                """ This is my hello world """
                print("Hello World!")


            @command("add-entry")
            @click.argument("name")
            def add_entry(name):
                """ Add new entry """
                print("Name: %s" % name)


### Running

    mocha

Running the code above will show the follow

    Commands:
      :addview                 Create a new view and template page
      :assets2s3               Upload assets files to S3
      :dbsync                  Sync database Create new tables etc...
      :init                    Setup Mocha in the current directory
      :install-assets          Install NPM Packages for the front end in the...
      :serve                   Serve application in development mode
      :version
      add-entry                Add new entry
      hello-world              This is my hellow word


If you run

    mocha hello-world

It will print out 'Hello World!'

And...

    mocha add-entry Jonas

will print out 'Name: Jonas'


### How does it work?

Mocha looks for all the subclasses of `mocha.cli.CLI` and instantiate them by
passing the `mocha.cli command` scope, along with `click`

### Importing application modules in the CLI

To import application modules, place them in `__init__` of the class, so Mocha
has the time to load all the necessary modules


    class MyCLI(mocha.cli.CLI):

        def __init__(self, command, click):

            import application.helpers as helpers

            @command('hello-world')
            def hello_world():
                """ This is my hello world """
                print("Hello World!")


