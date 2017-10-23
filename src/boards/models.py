"""
boards module models
"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from boards.managers import BoardsQuerySet
from zenboard.utils import github_api, zenhub_api


class Board(models.Model):
    """
    Model representation of a Zenhub, read only board. It specifies how should
    the ZenHub data be filtered and who should be able to access it.
    """
    name = models.SlugField(
        verbose_name='Name',
        unique=True,
    )

    github_repository = models.CharField(
        verbose_name='GitHub repository',
        max_length=255,
        help_text="In format: ':owner/:repo'."
    )

    github_repository_id = models.CharField(
        verbose_name='GitHub repository ID',
        max_length=255,
        editable=False,  # This gets populated from 'github_repository' field
    )

    github_labels = models.CharField(
        verbose_name='GitHub labels name',
        max_length=255,
        blank=True,
        help_text="Comma separated list of GitHub labels that will be used "
                  "to filter issues. If none provided, all issues will be "
                  "visible.",
    )

    filter_sign = models.CharField(
        verbose_name='filter sign',
        max_length=16,
        default='🐙',
    )

    include_epics = models.BooleanField(
        verbose_name='include Epic issues',
        default=False,
    )

    is_active = models.BooleanField(
        verbose_name='is active',
        default=True,
    )

    whitelisted_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='boards',
        verbose_name='whitelisted users',
        blank=True,
    )

    created = models.DateTimeField(
        verbose_name='created at',
        editable=False,
        auto_now_add=True,
    )

    modified = models.DateTimeField(
        verbose_name='modified at',
        editable=False,
        auto_now=True,
    )

    objects = BoardsQuerySet.as_manager()

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"
        get_latest_by = 'modified'
        ordering = ('-modified', '-created')

    def get_github_repository_client(self):
        """
        Helper method for getting GitHub repository client.

        :returns: GitHub repository client
        :rtype: github3.repos.Repository
        """
        owner, repo = self.github_repository.split('/')
        gh_repo = github_api.repository(owner, repo)

        return gh_repo

    def get_pipelines(self):
        """
        Get board pipelines data from ZenHub API.

        :returns: board pipeline list
        :rtype: list
        """
        pipelines = list()

        # We filter issues based on GitHub labels, so we have to first get
        # the list of allowed issues numbers and then use that to filter
        # data from ZenHub API
        gh_repo = self.get_github_repository_client()

        filtered_issues = dict()
        for issue in gh_repo.iter_issues(labels=self.github_labels):
            filtered_issues[issue.number] = {
                'title': issue.title,
                'state': issue.state,
            }

        filtered_issues_numbers = list(filtered_issues.keys())

        zenhub_board = zenhub_api.get_board(self.github_repository_id)

        # Zenhub doesn't track closed issues so we have to add them manually
        closed_filtered_issues_numbers = [
            issue_number
            for issue_number, issue in filtered_issues.items()
            if issue['state'] == 'closed'
        ]

        zenhub_board.append({
            'name': 'Closed',
            # This is to mimic ZenHub API response format
            'issues': [
                {'issue_number': issue_number}
                for issue_number in closed_filtered_issues_numbers
            ],
        })

        # Iterate through pipelines and their issues, filter them and get
        # their title
        for pipeline in zenhub_board:
            pipeline_issues = list()
            for issue in pipeline['issues']:
                if issue['issue_number'] in filtered_issues_numbers:
                    issue_number = issue['issue_number']
                    pipeline_issues.append({
                        'title': filtered_issues[issue_number]['title'],
                        'number': issue_number,
                        'is_epic': issue.get('is_epic', False),
                    })

            pipelines.append({
                'name': pipeline['name'],
                'issues': pipeline_issues
            })

        return pipelines

    def get_pipelines_cache_key(self):
        """
        Helper method for generating a unique key that's used when
        accessing pipelines data from cache.

        :returns: current board data unique cache key
        :rtype: str
        """
        return '{app_label}.{object_name}:{pk}:pipelines'.format(
            app_label=self._meta.app_label,
            object_name=self._meta.object_name,
            pk=self.pk,
        )

    def __str__(self):
        return '{0.name} board (PK: {0.pk})'.format(self)

    def get_absolute_url(self):
        return reverse('boards:details', kwargs={'name': self.name})

    def clean(self):
        """
        Extend Django's `clean` method and additional validation.
        """
        # Make sure that provided GitHub repo is valid and accessible
        try:
            gh_repo = self.get_github_repository_client()
            if not gh_repo:
                raise ValueError

            self.github_repository_id = gh_repo.id
        except AttributeError:
            raise ValidationError(
                "GitHub client isn't configured properly."
            )
        except ValueError:
            raise ValidationError({
                'github_repository': "Inaccessible GitHub repository."
            })

        # Strip any leading and trailing whitespace just to be safe
        self.github_labels = self.github_labels.strip()

        return super().clean()
