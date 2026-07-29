from django.core.management.base import BaseCommand

from baliyo.models import Project


class Command(BaseCommand):
    help = "Mark all projects (or a filtered subset) as 'published'."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show how many projects would be updated without actually updating them.",
        )
        parser.add_argument(
            "--status",
            type=str,
            default=None,
            help="Only update projects that currently have this status (e.g. 'in_progress').",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        current_status = options["status"]

        qs = Project.objects.all()

        if current_status:
            qs = qs.filter(status=current_status)
            self.stdout.write(f"Filtering projects with status='{current_status}' ...")

        count = qs.count()

        if count == 0:
            self.stdout.write(self.style.WARNING("No projects matched the criteria."))
            return

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"[DRY RUN] Would mark {count} project(s) as 'published'."
                )
            )
            for project in qs:
                self.stdout.write(f"  - [{project.status}] {project.title}")
            return

        updated = qs.update(status="published")
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully marked {updated} project(s) as 'published'."
            )
        )
