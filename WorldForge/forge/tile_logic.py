from forge.models import Tile


class AdjacentBlank(object):
    def __init__(self, h, v):
        self.h_pos = h
        self.v_pos = v
        self.adj = True

    def __repr__(self):
            return 'ADJ'

def get_matrix(tiles):
    try:
        # Set up max rows/max cols for the table
        max_h = 0
        min_h = 0
        max_v = 0
        min_v = 0

        for tile in tiles:
            if tile.horizontal_position > max_h:
                max_h = tile.horizontal_position
            if tile.horizontal_position < min_h:
                min_h = tile.horizontal_position
            if tile.vertical_position > max_v:
                max_v = tile.vertical_position
            if tile.vertical_position < min_v:
                min_v = tile.vertical_position

        num_rows = abs(max_h) + abs(min_h) + 1
        num_cols = abs(max_v) + abs(min_v) + 1

        max_rows = num_rows # Add 2 to rows/cols to have the outside squares available to add more
        max_cols = num_cols

        #  Set up a blank matrix based on the number of rows and columns needed
        tile_matrix = [ [[] for x in range(max_rows)] for y in range(max_cols)]

        #  Shift the position numbers for each tile over for easier printing
        for tile in tiles:
            tile.h_pos = tile.horizontal_position + abs(min_h)
            tile.v_pos = tile.vertical_position - abs(max_v)

        # Assign items to each list/tile position - will be the image file names for the large map output
        for y in range(len(tile_matrix)):
            for x in range(len(tile_matrix[y])):
                for tile in tiles:
                    if tile.h_pos == x and abs(tile.v_pos) == y:
                        tile_matrix[y][x] = tile

        # Add blank row/columns surrounding the matrix
        row_len = 0
        for row in tile_matrix:
            row.insert(0, [])
            row.append([])
            row_len = len(row)

        tile_matrix.insert(0, [[] for i in range(row_len)])
        tile_matrix.append([[] for i in range(row_len)])

    except Exception as e:
        print 'EXCEPTION', e
        tile_matrix = []

    # Specific blank adjacent cells (these will be the cells that can have tiles created within)
    tile_matrix = fill_adj_cells(tile_matrix)

    return tile_matrix

def print_matrix(tm):
    for row in tm:
        print row

def fill_adj_cells(tm):
    # Specify adjacent blank cells
    row_num = 0
    for row in tm:
        cell_num = 0
        for cell in row:
            # Check the cell above
        #if row_num != 0: # If not first row
            # If this cell is blank and the same cell in the row above is a Tile
            try:
                if cell == [] and isinstance(tm[row_num - 1][cell_num], Tile):
                    tile = tm[row_num - 1][cell_num]
                    h = tile.horizontal_position
                    v = tile.vertical_position - 1
                    tm[row_num][cell_num] = AdjacentBlank(h, v)
            except IndexError:
                pass

        # Check the cell below
        #if row_num != len(tm)-1: # if not last row
            try:
                if cell == [] and isinstance(tm[row_num + 1][cell_num], Tile):
                    tile = tm[row_num + 1][cell_num]
                    h = tile.horizontal_position
                    v = tile.vertical_position + 1
                    tm[row_num][cell_num] = AdjacentBlank(h, v)
            except IndexError:
                pass

        # Check the cell to the right
        #if cell_num != len(row)-1: # if not last cell
            try:
                if cell == [] and isinstance(tm[row_num][cell_num + 1], Tile):
                    tile = tm[row_num][cell_num + 1]
                    h = tile.horizontal_position - 1
                    v = tile.vertical_position
                    tm[row_num][cell_num] = AdjacentBlank(h, v)
            except IndexError:
                pass

        # Check the cell to the left
        #if cell_num != 0: # if not first cell
            try:
                if cell == [] and isinstance(tm[row_num][cell_num - 1], Tile):
                    tile = tm[row_num][cell_num - 1]
                    h = tile.horizontal_position + 1
                    v = tile.vertical_position
                    tm[row_num][cell_num] = AdjacentBlank(h, v)
            except IndexError:
                pass

            cell_num += 1
        row_num += 1

    return tm