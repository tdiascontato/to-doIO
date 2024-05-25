import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Personal_Development.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Error: manage.py"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
