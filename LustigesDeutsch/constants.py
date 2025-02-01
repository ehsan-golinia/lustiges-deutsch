MIN_SCORE = 6


MAX_DICE = 5

g_names = [
    'vokabel',
    'singular_plural',
    'artikel',
    'verb',
    'adjektiv',
    'partizip_II',
    'satz'
]


game_colors = {
    'green': 'success',
    'red': 'danger',
    'blue': 'primary',
    'yellow': 'warning',
}


cell_size = 52


board_data = [
                                {'value': 0, 'x': 2, 'y': 6, 'special': 'START'},
                                {'value': 1, 'x': 2, 'y': 5, 'special': '1'},
                                {'value': 2, 'x': 2, 'y': 4, 'special': '2'},
                                {'value': 3, 'x': 2, 'y': 3, 'special': '3'},
                                {'value': 4, 'x': 2, 'y': 2, 'special': '4'},
                                {'value': 5, 'x': 2, 'y': 1, 'special': '5'},
                                {'value': 6, 'x': 2, 'y': 0, 'special': '6'},
                                {'value': 7, 'x': 3, 'y': 0, 'special': '7'},
                                {'value': 8, 'x': 4, 'y': 0, 'special': '8'},
                                {'value': 9, 'x': 4, 'y': 1, 'special': '9'},
                                {'value': 10, 'x': 4, 'y': 2, 'special': '10'},
                                {'value': 11, 'x': 4, 'y': 3, 'special': '11'},
                                {'value': 12, 'x': 4, 'y': 4, 'special': '12'},
                                {'value': 13, 'x': 4, 'y': 5, 'special': '13'},
                                {'value': 14, 'x': 4, 'y': 6, 'special': '14'},
                                {'value': 15, 'x': 5, 'y': 6, 'special': '15'},
                                {'value': 16, 'x': 6, 'y': 6, 'special': '16'},
                                {'value': 17, 'x': 6, 'y': 5, 'special': '17'},
                                {'value': 18, 'x': 6, 'y': 4, 'special': '18'},
                                {'value': 19, 'x': 6, 'y': 3, 'special': '19'},
                                {'value': 20, 'x': 6, 'y': 2, 'special': '20'},
                                {'value': 21, 'x': 6, 'y': 1, 'special': '21'},
                                {'value': 22, 'x': 6, 'y': 0, 'special': '22'},
                                {'value': 23, 'x': 7, 'y': 0, 'special': '23'},
                                {'value': 24, 'x': 8, 'y': 0, 'special': '24'},
                                {'value': 25, 'x': 8, 'y': 1, 'special': '25'},
                                {'value': 26, 'x': 8, 'y': 2, 'special': '26'},
                                {'value': 27, 'x': 8, 'y': 3, 'special': '27'},
                                {'value': 28, 'x': 8, 'y': 4, 'special': '28'},
                                {'value': 29, 'x': 8, 'y': 5, 'special': '29'},
                                {'value': 30, 'x': 8, 'y': 6, 'special': 'END'}
                            ]
