

Mocha exposes some ex


    from mocha import exceptions

---

### MochaError

**MochaError** is raised when there is an error in the core of Mocha


---

### AppError


    class Index(Mocha):
        
        def error(self):
            try:
                # blah blah code
                raise exceptions.AppError('Something bad happened..')
            except exceptions.MochaError as ae:
                flash_error(ae.message)

---

### ModelError




