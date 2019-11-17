
## storage

Allows you to to access, upload, download, save and delete files on cloud
storage providers such as: AWS S3, Google Storage, Microsoft Azure,
Rackspace Cloudfiles, and even Local file system

#### Import

    from mocha import storage


#### Upload File


#### Delete File


#### Config

Edit the keys below in your config class file:

    #: STORAGE_PROVIDER:
    # The provider to use. By default it's 'LOCAL'.
    # You can use:
    # LOCAL, S3, GOOGLE_STORAGE, AZURE_BLOBS, CLOUDFILES
    STORAGE_PROVIDER = "LOCAL"

    #: STORAGE_KEY
    # The storage key. Leave it blank if PROVIDER is LOCAL
    STORAGE_KEY = AWS_ACCESS_KEY_ID

    #: STORAGE_SECRET
    #: The storage secret key. Leave it blank if PROVIDER is LOCAL
    STORAGE_SECRET = AWS_SECRET_ACCESS_KEY

    #: STORAGE_REGION_NAME
    #: The region for the storage. Leave it blank if PROVIDER is LOCAL
    STORAGE_REGION_NAME = AWS_REGION_NAME

    #: STORAGE_CONTAINER
    #: The Bucket name (for S3, Google storage, Azure, cloudfile)
    #: or the directory name (LOCAL) to access
    STORAGE_CONTAINER = os.path.join(APPLICATION_DATA_DIR, "uploads")

    #: STORAGE_SERVER
    #: Bool, to serve local file
    STORAGE_SERVER = True

    #: STORAGE_SERVER_URL
    #: The url suffix for local storage
    STORAGE_SERVER_URL = "files"



### storage.get

Allows you to get a file from the storage

    my_file = storage.get("myfile.jpg")

    my_file.name  # return The file name

    my_file.size  # returns file size


### storage.upload
