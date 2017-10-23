# Zenboard
[![Build status](https://img.shields.io/travis/pawelad/zenboard.svg)][travis]
[![GitHub release](https://img.shields.io/github/release/pawelad/zenboard.svg)][github]
[![Test coverage](https://img.shields.io/coveralls/pawelad/zenboard.svg)][coveralls]
[![License](https://img.shields.io/github/license/pawelad/zenboard.svg)][license]

Zenboard is a straightforward Django application that gives you the ability to
create read only [ZenHub][zenhub] boards that you can share with other people
without the need to give them access to your GitHub repository.

Still a work in progress.

Based on proof of concept by @kuuji - https://github.com/kuuji/dashub

## Running it locally
Take a look [here][running locally] if you want to run Zenboard locally and
feel free to [open an issue][zenboard new issue] if you'r having any problems.

## Contributions
Feel free to use, ask, fork, star, report bugs, fix them, suggest enhancements,
add functionality and point out any mistakes. Thanks!

## Tests
Package was tested with the help of `pytest` and `tox` on Python 3.6 with
Django 1.11 and Django REST Framework 3.7 (see `tox.ini`).

Code coverage is available at [Coveralls][coveralls].

To run tests yourself you need to set environment variable with Django secret
key before running `tox` inside the repository:

```shell
$ export SECRET_KEY='...'
$ pip install tox
$ tox
```

## Authors
Developed and maintained by [Paweł Adamczak][pawelad].

Released under [Apache License 2.0][license].


[coveralls]: https://coveralls.io/github/pawelad/zenboard
[github]: https://github.com/pawelad/zenboard
[license]: https://github.com/pawelad/zenboard/blob/master/LICENSE
[pawelad]: https://github.com/pawelad
[running locally]: https://github.com/pawelad/zenboard/wiki/Running-Zenboard-locally
[travis]: https://travis-ci.org/pawelad/zenboard
[zenboard new issue]: https://github.com/pawelad/zenboard/issues/new
[zenhub]: https://www.zenhub.com/
