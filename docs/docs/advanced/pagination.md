
## Overview

Assembly uses the Paginator to paginate iterable items

---

## Usage

---

### Paginate Models

Paginate models

```

from assembly import Assembly, models, request

class Index(Assembly):

    def posts(self):
        per_page = 10
        page = int(request.args.get("page", 1))

        posts = models.Posts.query()

        posts = posts.paginate(page=page, per_page=per_page)

        return {
            "posts": posts
        }

```



---

### Paginate List

To paginate a list of items

```

from assembly import Assembly, request
from paginator import Paginator

class Index(Assembly):

    def posts(self):
        per_page = 10
        page = int(request.args.get("page", 1))

        items = range(1, 1000)
        items = Paginator(items, page=page, per_page=per_page)

        return {
            "items": [i for i in items]
        }




```

---

## API

---
