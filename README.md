<p align="center">
  <img src="https://cdn.rawgit.com/pawelad/zenboard/abbb7917/src/zenboard/static/img/logo.png" alt="Zenboard logo">
</p>

[![Build status](https://img.shields.io/travis/pawelad/zenboard.svg)][travis]
[![GitHub release](https://img.shields.io/github/release/pawelad/zenboard.svg)][github]
[![Test coverage](https://img.shields.io/coveralls/pawelad/zenboard.svg)][coveralls]
[![License](https://img.shields.io/github/license/pawelad/zenboard.svg)][license]

Zenboard is a straightforward Django application that gives you the ability to
create read only [ZenHub][zenhub] boards.

Based on proof of concept by [@kuuji][kuuji] - [kuuji/dashub][kuuji dashub]

Usable at the moment, but very much a work in progress.

## High level overview
Zenboard aims to provide an easy way to create a filtered and read only views
of a Zenhub boards. It's currently used to give customers an overview of their
issues that doesn't require double lifting (we already use ZenHub to track 
that), allows specifying exactly which issues and comments should be visible,
and can be used without a GitHub account.

Caching is built in and a priority because of the sheer number of requests to
both ZenHub and GitHub APIs needed to generate the board view.

See [TODO.md][todo list] for current, loose roadmap.

## Running Zenboard
Take a look [here][running zenboard] if you want to run Zenboard yourself,
either locally or in production, and [open an issue][zenboard new issue] if
you have any questions or problems.

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
$ pip install tox
$ export SECRET_KEY='...'
$ tox
```

## Authors
Developed and maintained by [Paweł Adamczak][pawelad].

Released under [Apache License 2.0][license].


[coveralls]: https://coveralls.io/github/pawelad/zenboard
[github]: https://github.com/pawelad/zenboard
[kuuji]: https://github.com/kuuji
[kuuji dashub]: https://github.com/kuuji/dashub
[license]: https://github.com/pawelad/zenboard/blob/master/LICENSE
[pawelad]: https://github.com/pawelad
[running zenboard]: https://github.com/pawelad/zenboard/wiki/Running-Zenboard
[todo list]: https://github.com/pawelad/zenboard/blob/master/TODO.md
[travis]: https://travis-ci.org/pawelad/zenboard
[zenboard new issue]: https://github.com/pawelad/zenboard/issues/new
[zenhub]: https://www.zenhub.com/
