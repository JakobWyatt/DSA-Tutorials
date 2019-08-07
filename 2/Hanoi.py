import typing
import sys

def towers(n : int, src : int, dest : int) -> None:
    if n == 1:
        moveDisk(src, dest)
    else:
        tmp = 6 - src - dest
        towers(n - 1, src, tmp)
        moveDisk(src, dest)
        towers(n - 1, tmp, dest)

def moveDisk(src : int, dest : int) -> None:
    print(f"Moving top disk from peg {src} to peg {dest}")

if __name__ == "__main__":
    towers(*[int(x) for x in sys.argv[1:]])
