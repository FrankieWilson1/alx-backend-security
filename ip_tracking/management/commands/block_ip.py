from django.core.management.base import BaseCommand

from ...models import BlockedIP

class Command(BaseCommand):
    """
    Command to block an IP address.
    """
    help = "Blocks a specified IP address from accessing the site."

    def add_arguments(self, parser):
        parser.add_argument(
            'ip_address', type=str, help="The IP address to block"
        )
        parser.add_argument(
            '--reason', type=str, help="The reason for blocking this IP",
            default=''
        )

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        reason = options['reason']

        try:
            BlockedIP.objects.create(
                ip_address=ip_address,
                reason=reason
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully blocked IP: {ip_address}")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Failed to block IP: {ip_address}.\
                    Error: {str(e)}")
            )
