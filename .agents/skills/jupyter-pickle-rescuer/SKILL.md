---
name: jupyter-pickle-rescuer
description: >-
  Automatically injects monkey-patching workarounds into batch processing scripts 
  to rescue and load pickled class instances that were originally serialized inside 
  interactive Jupyter Notebooks.
---

# Jupyter Pickle Rescuer

## Overview
When data objects (like custom classes) are pickled inside an interactive Jupyter Notebook, Python stamps them with the `<module '__main__'>` namespace. When you later attempt to load these pickles from a standalone background CLI script or module, `pickle.load()` crashes with `AttributeError: Can't get attribute 'MyClass' on <module '__main__'>`. This skill provides a standard protocol to intercept and rescue these pickles without having to rebuild the data.

## Dependencies
- None.

## Quick Start
"I'm getting an AttributeError for SessionStore when trying to load my pickle data in this script."

## Workflow

### 1. Identify the Target Class
- Locate the custom class that is failing to load (e.g., `SessionStore`).
- Identify where that class is actually defined in the current script's namespace (e.g., imported from `utils.py`).

### 2. Monkey-Patch `__main__`
- At the top of the script (or right before the `pickle.load()` call), import the built-in `__main__` module.
- Explicitly map the imported class into the `__main__` namespace so the `pickle` unpickler can find it.

### 3. Implementation Template
Inject the following pattern into the script:
```python
# Import the class from its actual location
from utils import MyClass

# Rescue Jupyter-generated pickles
import __main__

__main__.MyClass = MyClass

# Now it is safe to load
data = pickle.load(file_handle)
```

## Common Mistakes
- **Rebuilding the data**: Do not tell the user they have to go back to the Jupyter notebook and re-pickle the data or export to JSON unless this workaround fundamentally fails. Always try rescuing the pickle first.
