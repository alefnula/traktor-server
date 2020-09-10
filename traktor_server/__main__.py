from pathlib import Path
from tea_django.main import Main


main = Main("traktor-server", app_dir=Path(__file__).parents[1])


if __name__ == "__main__":
    main()
