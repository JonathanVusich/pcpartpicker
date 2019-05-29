from pcpartpicker.api import API


def main():
    api = API()
    api.set_multithreading(False)
    part_data = api.retrieve_all()
    for data in part_data.values():
        for part in data:
            assert not part.model == ""


if __name__ == "__main__":
    main()
