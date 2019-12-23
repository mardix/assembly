
## Overview

Aseembly uses Flask-Cloudy to let you access, upload, download, save and delete files on cloud
storage providers such as: AWS S3, Google Storage, Microsoft Azure,
Rackspace Cloudfiles, and even Local file system.

Extension: <a href="https://github.com/mardix/flask-cloudy" target="_blank">flask-cloudy</a>

---

## Usage

```python
from assembly import get_file, upload_file, download_file, delete_file
```

**get_file**, **upload_file**, **download_file**, **delete_file** are part of functions to work with files.


---


### Get file

`get_file` will return a Storage Object.

```python
from assembly import get_file

myfile = get_file("hello.txt")

myfile.name  # return The file name
myfile.size  # returns file size
myfile.full_url # the full url of the file

```

---

### Upload file

`upload_file` to save or upload a file in the container

#### Example of file upload

```python
# views/main.py

from assembly import Assembly, upload_file, request, redirect

class Index(Assembly):

    def index(self):
        return

    @request.post
    def upload(self):
        file = request.files.get("file")
        if file:
            profile_image = upload_file(file,
                                        name=utils.gen_uuid(),
                                        prefix="img.",
                                        public=True,
                                        extensions=["jpg", "jpeg", "png", "gif"])
        return redirect(self.upload_success)

    def upload_success(self):
        return "Upload successful!" 

```

Template


```html
<!-- templates/main/Index/index.html -->

{% extends 'layouts/base.html' %}

{% block title %}Upload{% endblock %}

{% block body %}
    <h1>Upload</h1>
    <form id="uploadbanner" action="/upload/" enctype="multipart/form-data" method="post">
        <input type='hidden' name="_csrf_token" value='{{ csrf_token() }}'>
        <input id="fileupload" name="file" type="file" />
        <input type="submit" value="Upload" id="submit" />
     </form>    

{% endblock %}

```

**Note**: Since this will call a POST, we also add the CSRF token in the form

```html
<input type='hidden' name="_csrf_token" value='{{ csrf_token() }}'>
```

#### Signal

`upload_file` emits a signal to be used

```python
from assembly import upload_file

@upload_file.post
def file_uploaded(result, **kw):
    if result:
        print("File uploaded successfully!")

```

---

### Download File

`download_file` to download a file to the user. You will need to redirect to that path.

```python
from assembly import Assembly, download_file, redirect

class Index(Assembly):

    def dowload(self):
        filename = "hello.txt"
        name = "new-name-hello"
        url = download_file(filename, name=name, timeout=60)
        return redirect(url)

```

#### Signal

`download_file` emits a signal to be used

```python
from assembly import download_file

@download_file.post
def file_downloaded(result, **kw):
    if result:
        print("File uploaded successfully!")

```

---

### Delete File

`delete_file` deletes a file from storage


```python
from assembly import delete_file 

delete_file("hello.txt")

```

#### Signal

`delete_file` emits a signal to be used

```python
from assembly import delete_file

@delete_file.post
def file_deleted(result, **kw):
    if result:
        print("File deleted successfully!")

```

---

## Config

```python
# config.py

STORAGE = {
    #: STORAGE_PROVIDER:
    # The provider to use. By default it's 'LOCAL'.
    # You can use:
    # LOCAL, S3, GOOGLE_STORAGE, AZURE_BLOBS, CLOUDFILES
    "PROVIDER": "LOCAL",

    #: STORAGE_KEY
    # The storage key. Leave it blank if PROVIDER is LOCAL
    "KEY": AWS_ACCESS_KEY_ID,

    #: STORAGE_SECRET
    #: The storage secret key. Leave it blank if PROVIDER is LOCAL
    "SECRET": AWS_SECRET_ACCESS_KEY,

    #: STORAGE_REGION_NAME
    #: The region for the storage. Leave it blank if PROVIDER is LOCAL
    "REGION_NAME": AWS_REGION_NAME,

    #: STORAGE_CONTAINER
    #: The Bucket name (for S3, Google storage, Azure, cloudfile)
    #: or the directory name (LOCAL) to access
    "CONTAINER": os.path.join(DATA_DIR, "uploads"),

    #: STORAGE_SERVER
    #: Bool, to serve local file
    "SERVER": True,

    #: STORAGE_SERVER_URL
    #: The url suffix for local storage
    "SERVER_URL": "files",

    #:STORAGE_UPLOAD_FILE_PROPS
    #: A convenient K/V properties for storage.upload to use when using `upload_file()`
    #: It contains common properties that can passed into the upload function
    #: ie: upload_file("profile-image", file)
    "UPLOAD_FILE_PROPS": {
        # To upload regular images
        "image": {
            "extensions": ["jpg", "png", "gif", "jpeg"],
            "public": True
        },

        # To upload profile image
        "profile-image": {
            "prefix": "profile-image/",
            "extensions": ["jpg", "png", "gif", "jpeg"],
            "public": True
        }
    }

}

```

---

## Storage Object

The class **Object** is an entity of an object in the container.

Usually, you will get a cloud object by accessing an object in the container.

```python
my_object = get_file("my_object.txt")
```	

Properties and Methods:
	
- Object.name: The name of the object
- Object.size: The size in bytes of the object
- Object.extension: The extension of the object
- Object.url: Return the url of the object
- Object.full_url: Returns the full url of the object
- Object.secure_url:Return a secured url, with **https://** 
- Object.path: The path of the object relative to the container
- Object.full_path: For Local, it will show the full path of the object, otherwise it just returns the Object.path
- Object.provider_name: The provider name: ie: Local, S3,...
- Object.type: The type of the object, ie: IMAGE, AUDIO, TEXT,... OTHER
- Object.info: Returns a dict of the object name, extension, url, etc. This can be saved in a DB
- Object.save_to: (method) to save to a destination
- Object.download_url: (method) Return a URL that triggers the browser download of the file. On cloud providers it will return a signed url.

---
