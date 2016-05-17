import csv
import argparse
import os
import glob
import shutil

import numpy
import matplotlib.pyplot as plot

BLACK_CHAR = '0'
WHITE_CHAR = '1'
BLACK_INDEX = 0
WHITE_INDEX = 1

parser = argparse.ArgumentParser(description='Process (and visualize) game logs')
parser.add_argument('directory', metavar='game_logs_directory', type=str, help='The folder containing the CSV game logs')
parser.add_argument('--filter', metavar='ai_name', dest='filter', action='store', help='AI name by which to filter')

args = parser.parse_args()

if not os.path.isdir(args.directory):
    print("Not a directory (or does not exist: %s" % args.directory)
    exit(1)

if os.path.isdir('graphs'):
    shutil.rmtree('graphs')
os.mkdir('graphs')

for game_log_file_name in glob.glob(os.path.join(args.directory, 'akc-roundrobin_game_*.csv')):
    with open(game_log_file_name, newline='') as game_log_file:
        csv_reader = csv.reader(game_log_file, delimiter=';')

        winner_index = None
        players = []
        black_moves = []
        white_moves = []
        target_player_color = None

        header = True
        block_index = 0
        for row_index, row in enumerate(csv_reader):
            if header:
                header = False
                continue

            if len(row) == 0:
                block_index += 1
                header = True
                continue

            # game & player info
            if block_index == 1:
                players.append({
                    "color": "black" if row[0] == BLACK_CHAR else "white",
                    "seed": int(row[1]),
                    "name": row[2]
                })

            # actual game
            elif block_index == 2:
                if row[0] == 'end':
                    continue

                if row[1] == BLACK_CHAR:
                    black_moves.append([int(row[2]), int(row[6])])
                else:
                    white_moves.append([int(row[2]), int(row[6])])

            elif block_index == 3:
                winner_index = BLACK_INDEX if row[4] == '1' else WHITE_INDEX
                break

        player_names = [player['name'] for player in players]

        if args.filter is not None:
            if args.filter not in player_names:
                continue

            target_player_color = BLACK_CHAR if player_names.index(args.filter) == BLACK_INDEX else WHITE_CHAR

        black_moves = numpy.array(black_moves)
        white_moves = numpy.array(white_moves)

        black_line_style = '-' if target_player_color == BLACK_CHAR else '--'
        white_line_style = '-' if target_player_color == WHITE_CHAR else '--'

        fig, time_left_axis = plot.subplots()
        black_time_left_line, = time_left_axis.plot(range(len(black_moves)), black_moves[:, 0], 'b' + black_line_style, label=BLACK_CHAR)
        white_time_left_line, = time_left_axis.plot(range(len(white_moves)), white_moves[:, 0], 'b' + white_line_style, label=WHITE_CHAR)
        time_left_axis.set_xlabel('turn')

        time_left_axis.set_ylabel('remaining time', color='b')
        time_left_axis.set_ylim([0, 120000])
        for tl in time_left_axis.get_yticklabels():
            tl.set_color('b')

        time_per_move_axis = time_left_axis.twinx()
        time_per_move_axis.plot(range(len(black_moves)), black_moves[:, 1], 'r' + black_line_style, label=BLACK_CHAR)
        time_per_move_axis.plot(range(len(white_moves)), white_moves[:, 1], 'r' + white_line_style, label=WHITE_CHAR)
        time_per_move_axis.set_ylabel('time per move', color='r')
        for tl in time_per_move_axis.get_yticklabels():
            tl.set_color('r')

        end_line = time_left_axis.axvline(x=len(black_moves) - 1, color='g')

        labels = ["%s (%d)" % (player['name'], player['seed']) for player in players]
        labels.append('Game won by %s' % player_names[winner_index])

        # box = time_left_axis.get_position()
        # time_left_axis.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
        legend = fig.legend(
            handles=[black_time_left_line, white_time_left_line, end_line],
            labels=labels,
            ncol=3,
            loc='upper center'
        )
        plot.savefig(
            os.path.join('graphs', game_log_file_name.split('/')[1].split('.')[0] + '.png'),
            bbox_extra_artists=(legend, ),
            bbox_inches='tight'
        )

        plot.close(fig)




