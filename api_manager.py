from pcpartpicker import API
import asyncio

def main():
    api = API()
    api.retrieve_all()
    print(api._scraper.cpu)

if __name__ == "__main__":
    main()