def binary : 1 (x y) y;
def average(x y) (x + y) * 0.5;

def main(x y)
  x = 1
  : y = 2
  : average(x, y)
  : x = 3
  : y = 5
  : average(x, y)
  ;

main(0, 0);
