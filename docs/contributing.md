# Contributing to SerialBus

First off, thank you for considering contributing to SerialBus.

If you've noticed a bug or have a feature request, make one! It's generally best if you get confirmation of your bug or approval for your feature request this way before starting to code.


## Fork & create a branch

If this is something you think you can fix, then fork and create a branch with a descriptive name.

A good branch name would be (where issue #325 is the ticket you're working on):

```bash
git checkout -b 325-add-support-for-xyz
```

## Test your changes
It's important to make sure your changes don't break anything. Run the project's tests before you commit your changes.

> NOTE: if you are adding a new feature, make sure you are also adding specific tests for it, otherwise your PR will not be accepted.


Once you are good for tests, just run `pytest` from the root directory of the project.

```bash
pytest
```

## Submit a pull request
Go to your fork on GitHub and click the "New pull request" button. Fill out the form, and then click "Create pull request".

And you're done! Your changes will be reviewed as soon as possible. 

A million thanks you for your contribution! 🚌