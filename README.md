# JuzzyPython
## Python implementation of Christian Wagner's Juzzy

Please refer to **[Juzzy](http://juzzy.wagnerweb.net/)** for Java and online implementations

### Installation:

You can install this package using pip. 

In the root directory (Where setup.py exists), please type:

`pip3 install .`

You can then import Juzzy through juzzyPython.

### HTML Documentation:

You can find detailed documentation on a browsable site in the following directory:

`juzzyPython/docs/build/html/index.html`

If files are edited, please navigate to:

`juzzyPython/docs`

and use

`make html`

to rebuild the documentation with your edits. 

### Examples:

You can run examples by importing from:

`juzzyPython.examples`

Examples can be run by calling the class:

```python
from juzzyPython.examples.SimpleT1FLS import SimpleT1FLS
SimpleT1FLS()
```

Or by running the file itself:

`python3 SimpleT1FLS.py`

The following examples are included:

SimpleT1FLS                             | Executes a type-1 fuzzy system example.
SimpleNST1FLS                           | Executes a non-singleton type-1 fuzzy system example.
SimpleT1FLS_twoOutputs                  | Executes a type-1 fuzzy system example with 2 outputs.
SimpleIT2FLS                            | Executes an interval type-2 fuzzy system example.
SimpleNST1IT2FLS                        | Executes a non-singleton type-1 interval type-2 fuzzy system example.
SimpleNSIT2_IT2FLS                      | Executes a non-singleton IT2 interval type-2 fuzzy system example.
SimpleIT2FLS_twoOutputs                 | Executes an interval type-2 fuzzy system example with 2 outputs.
SimplezGT2FLS                           | Executes a general type-2 fuzzy system example.
SimplezGT2FLSNST1                       | Executes a non-singleton type-1 general type-2 fuzzy system example.
SimplezGT2FLSNSIT2                      | Executes a non-singleton IT2 general type-2 fuzzy system example.
SimplezGT2FLSNSGT2                      | Executes a non-singleton GT2 general type-2 fuzzy system example.
SimplezGT2FLS_multicore                 | Executes a multi-threaded / multi-core general type-2 fuzzy system example.
SimplezGT2FLS_multicore_twoOutputs      | Executes a multi-threaded / multi-core general type-2 fuzzy system example with 2 outputs.