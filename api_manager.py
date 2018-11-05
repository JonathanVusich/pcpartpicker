from pcpartpicker import API
import asyncio

def main():
    api = API()
    result = asyncio.get_event_loop().run_until_complete(api._scraper._retrieve_part_data('cpu'))
    print('hi')

if __name__ == "__main__":
    main()