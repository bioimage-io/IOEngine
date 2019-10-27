# BioEngine

## Engine API

  * api.register
  *

## Development

- Install the packages needed for development.

  ```
  pip install -r requirements_dev.txt
  ```

- Run `tox` to test and lint the code.

  ```
  tox
  ```

- We use black code formatter to format the code automatically.

  ```
  black ./
  ```

- To test it, run:

  ```
  pip install -e .
  python bioengine/engine.py
  ```
