# TODO
Mostly for me, but feel free to contribute
([if that's what you're in to][if you're into it]):

- Integrate GitHub and Zenhub webhooks to update data only on change. This is
  a must and will enable us to always have up to date data and drop
  'force_refresh', which takes ages because of all the data processing we do.
- Rework boards permissions system, possibly with `django-guardian`.
- Tests. 'Nuff said.
- User management (the ability to invite a user) and password recovery.
- Add the ability to generate secret (but publicly available) board sharing links.
- Add proper, reusable Bootstrap 4 form handling - ideally with a third party library.


[if you're into it]: https://youtu.be/uRJZfwDgNTM?t=4
