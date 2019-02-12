# Google Cloud Datastore Utils

Utilities for Google Cloud Datastore.


# Installation

Simply run:

    $ pipsi install gcdu

You need to authenticate in the project using gcloud sdk:

    $ gcloud auth application-default login
    $ gcloud config set project PROJECT_ID

Or exporting the environment variable:

    $ export GOOGLE_APPLICATION_CREDENTIALS='key.json'

More help in this link https://developers.google.com/identity/protocols/application-default-credentials

---

# Usage

To use it:

    $ gcdu --help

Export command:

    $ gcdu export -p [project] -n [namespace] -k [comma separated list of datastore kinds]

Import command:

    $ gcdu import -p [project] -n [namespace] -k [comma separated list of datastore kinds]

