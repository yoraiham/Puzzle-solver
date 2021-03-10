import itertools
import operator
import cv2 as cv

def most_common(L):
  # get an iterable of (item, iterable) pairs
  SL = sorted((x, i) for i, x in enumerate(L))
  # print 'SL:', SL
  groups = itertools.groupby(SL, key=operator.itemgetter(0))
  # auxiliary function to get "quality" for an item
  def _auxfun(g):
    item, iterable = g
    count = 0
    min_index = len(L)
    for _, where in iterable:
      count += 1
      min_index = min(min_index, where)
    # print 'item %r, count %r, minind %r' % (item, count, min_index)
    return count, -min_index
  # pick the highest-count/earliest item
  return max(groups, key=_auxfun)[0]

def piece_to_coaards(piece_num):
    return (piece_num % 6) +1, int(piece_num / 6) + 1


def move_on_frame(cur_round):
    if cur_round >= 0 and cur_round <=7:
        return cur_round,0
    elif cur_round >=8 and cur_round <= 12:
        return 7, cur_round -7
    elif cur_round >= 13 and cur_round <= 19:
        return 19 - cur_round ,5
    else:
        return 0, 24 - cur_round



def translate(value, image_width, num_pieces_in_row, image_height, num_pieces_in_col):
    # Figure out how 'wide' each range is

    # convert width first
    # Convert the left range into a 0-1 range (float)
    widthScaled = float(value[0]) / float(image_width)
    heightScaled = float(value[1]) / float(image_height)

    # Convert the 0-1 range into a value in the right range.
    return ((int)(widthScaled * num_pieces_in_row) , (int)(heightScaled * num_pieces_in_col))



def draw_lines_on_photo(image, pieces_in_row, pieces_in_colomn):
    for i in range(pieces_in_row):
        x = int(i * (image.shape[1] / pieces_in_row))
        cv.line(image,(x,0), (x, image.shape[0]), (255,0,0),2)
    for i in range(pieces_in_colomn):
        y = int(i * (image.shape[0] / pieces_in_colomn))
        cv.line(image,(0,y), (image.shape[1], y), (255,0,0),2)
    return image
