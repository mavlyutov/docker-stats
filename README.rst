docker-stats
============

docker stats wrapper which prints output in json


Usage
=====

Install from PyPI and run ::

        usage: docker-stats [-h] [-a] [container [container ...]]

        docker stats, json way

        positional arguments:
          container   IDs or NAMEs of desired containers

        optional arguments:
          -h, --help  show this help message and exit
          -a, --all   get stats of all available containers
          -n, --normalize   try to normalize stats


Normalization
=============

Raw output of docker-stats is smth like this:

.. code-block:: javascript

    {
        "my_container": {
            "blkio_stats": {
                "io_merged_recursive": [],
                "io_queue_recursive": [],
                "io_service_bytes_recursive": [
                    {
                        "major": 253,
                        "minor": 5,
                        "op": "Read",
                        "value": 7020544
                    },
                    {
                        "major": 253,
                        "minor": 5,
                        "op": "Write",
                        "value": 0
                    },
                    *SNIP*
                ]
            }
        }
    }

As one can mention, there are an array object inside key :code:`io_service_bytes_recursive` and each element of that array is flattened JSON with key :code:`op` within values. That behaviour may occur in other keys.
docker-stats called with key :code:`--normalize` tries to jsonify that to:

.. code-block:: javascript

    {
        "my_container": {
            "blkio_stats": {
                "io_merged_recursive": [],
                "io_queue_recursive": [],
                "io_service_bytes_recursive": {
                    "Read": {
                        "major": 253,
                        "minor": 5,
                        "value": 7020544
                    },
                    "Write": {
                        "major": 253,
                        "minor": 5,
                        "value": 0
                    },
                    *SNIP*
                }
            }
        }
    }
