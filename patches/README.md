# Patch for using TI.GPIO with gpiozero library

The gpiozero library allows for using a custom pin factory. The sections below
describe the steps in applying a patch so that the TI.GPIO library pin definition
could be used with the gpiozero library.

# Cloning and patching gpiozero library

The easiest way to install this library is using `pip3`:
```shell
# Clone the gpiozero git project
git clone https://github.com/gpiozero/gpiozero.git

# Apply the patch
cd gpiozero

# The patch to be applied has been created for a specific commit on the
# master branch so make sure to checkout a branch with that commit.
git branch -f ti_gpio_patch 2b6aa5314830fedf3701113b6713161086defa38

# Apply the patch
git apply <path_to_ti-gpio_py root>/patches/gpiozero.patch
pip3 install .
```

