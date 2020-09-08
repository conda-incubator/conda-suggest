# Conda-Suggest Change Log



<!-- current developments -->

## v0.1.1
**Added:**

* New `write` flag added to `generate_map()` to enable disabling of
  actually writing the file.
* The `generate_map()` function now returns the contents of the map file.
* Added `remove_exprs` keyword argument to `generate_map()` to allow for
  filtering out command names. This defaults to removing `__pycache__`.
* New `--remove-exprs` command line option added to generate subcommand.

**Fixed:**

* Fixed Windows type error when matching against `.exe` and `.bat` files.

**Authors:**

* Anthony Scopatz
* Duncan Macleod



## v0.1.0
**Authors:**

* Anthony Scopatz


