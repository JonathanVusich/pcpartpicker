from pcpartpicker import API
from pcpartpicker.parts import CPU
import asyncio

def main():
    api = API()
    api.retrieve_all()
    print(api._scraper.cpu)

if __name__ == "__main__":
    main()