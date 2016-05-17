# antiking-chess-ai-analysis

## Usage

	usage: main.py [-h] [--filter ai_name] game_logs_directory

	Process (and visualize) game logs

	positional arguments:
	  game_logs_directory  The folder containing the CSV game logs

	optional arguments:
	  -h, --help           show this help message and exit
	  --filter ai_name     AI name by which to filter

## Usage example

    python3 main.py --filter Group06BasicKI game-logs-server/

## Output

The folder `./graphs/` is created (and overriden). In there you find a `*.png` for each game that matches the filter.
