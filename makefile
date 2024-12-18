all: black coverage

black:
	black .

coverage:
	coverage run --source aoc_utils -m unittest
	coverage report -m --fail-under 80

