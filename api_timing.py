from pcpartpicker import API
import time


def main():
    api = API()
    start = time.perf_counter()
    part_data = api.retrieve_all()
    print(time.perf_counter()-start)


if __name__ == "__main__":
    main()