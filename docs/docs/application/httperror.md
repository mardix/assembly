

HTTPError


```
from assembly import HTTPError
```

---

#### abort

#### BadRequest

400

#### Unauthorized

401

#### Forbidden

403

#### NotFound

404

#### MethodNotAllowed

405

#### NotAcceptable

406

#### RequestTimeout

408


#### Conflict

409

#### Gone

410

#### LengthRequired

411

#### PreconditionFailed

412

#### RequestEntityTooLarge

413

#### RequestURITooLarge

414

#### UnsupportedMediaType

415

#### RequestedRangeNotSatisfiable

416

#### ExpectationFailed

417

#### ImATeapot

418

#### UnprocessableEntity

422

#### Locked

423

#### FailedDependency

424

#### PreconditionRequired

428

#### TooManyRequests

429

#### RequestHeaderFieldsTooLarge

431

#### UnavailableForLegalReasons

451

#### InternalServerError

500

#### NotImplemented

501

#### BadGateway

502

#### ServiceUnavailable

503

#### GatewayTimeout

504

#### HTTPVersionNotSupported

505

#### ClientDisconnected

#### SecurityError


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




