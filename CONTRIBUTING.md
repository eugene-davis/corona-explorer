# Contributing

Contributions are welcome, and they are greatly appreciated. Every
little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/eugene-davis/corona-explorer/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and
"help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with
"enhancement" and "help wanted" is open to whoever wants to implement
it.

### Write Documentation

corona-explorer could always use more documentation,
whether as part of the official corona-explorer docs,
in docstrings, or even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at
https://github.com/eugene-davis/corona-explorer/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

## Get Started

Ready to contribute? Here's how to set up **corona-explorer** for local development.

1. Fork the **corona-explorer** repository.

1. Clone your fork locally.

1. Install your local copy into a virtualenv. Assuming you have virtualenv installed,
   this is how you set up your fork for local development:

        $ cd corona-explorer/
        $ virtualenv --python=python3 env
        $ source env/bin/activate
        $ pip install -r requirements_dev.txt
        $ python setup.py develop

1. Create a branch for local development and start making your changes locally:

        $ git checkout -b name-of-your-bugfix-or-feature

1. When you're done making changes, check that your changes pass pylint and the tests:

        $ python setup.py lint
        $ python setup.py test

1. Commit your changes and push your branch to Github:

        $ git add .
        $ git commit -m "Your detailed description of your changes."
        $ git push origin name-of-your-bugfix-or-feature-branch

1. Submit a pull request through the Github website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.

    We recommend using [py.test](http://pytest.org/en/latest/) over [unittest](https://docs.python.org/3/library/unittest.html) as it has a much simpler syntax and uses already built-in features (eg. assert).
    Please have a look as well on the [Hitchhikers's Guide to Python](https://docs.python-guide.org/writing/tests/) which gives many rules that
    should be followed while writing tests.
1. If the pull request adds functionality, the docs should be updated.

   Put your new functionality into a function with a docstring, and add the feature to the list in the [README.md](README.md).
1. The pull request should pass the CI checks. Check https://dev.azure.com/eugene-davis/gh-emd/_build and make sure that the tests pass for all supported Python versions.

## Tips

To run a subset of tests:

    $ py.test tests/test_corona_explorer.py

## Deploying

Deployment can only be done by the project maintainers and is done on-demand via the Azure CI.

Select the [corona-explorer build pipeline](https://dev.azure.com/eugene-davis/gh-emd/_build) and click
on the **Queue** button and run a build with the following settings:

* Branch: `master`
* Commit: leave it empty
* Variables:
  * `release: true`
