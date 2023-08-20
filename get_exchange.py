import aiohttp
import asyncio
from datetime import datetime, timedelta
import platform
import sys

CURRENCY = ['USD', 'EUR']
MAX_DAYS = 10

async def fetch_currency_data(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Error status: {response.status} for {url}")
    except aiohttp.ClientConnectorError as err:
        print(f'Connection error: {url}', str(err))
    return None

def transform_currency_data(currency_rates):
    transformed_data = []
    for rate in currency_rates['exchangeRate']:
        if rate['currency'] in CURRENCY:
            rates = {
                'sale': rate['saleRate'],
                'purchase': rate['purchaseRate']
            }
            transformed_data.append({currency_rates['date']: {rate['currency']: rates}})
    return transformed_data

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_currency_data(session, url) for url in urls]
        currency_data = await asyncio.gather(*tasks)
        
        transformed_data = []
        for data in currency_data:
            if data:
                transformed_data.extend(transform_currency_data(data))
        
        print(transformed_data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <num_days>")
        sys.exit(1)
    
    try:
        count = int(sys.argv[1])
        if count <= 0 or count > MAX_DAYS:
            print(f'Enter num from 1 to {MAX_DAYS}')
            sys.exit(1)
    except ValueError:
        print(f'Enter a valid integer')
        sys.exit(1)

    base_url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
    end_date = datetime.now() - timedelta(days=1)
    num_days = count
    urls = [f"{base_url}{(end_date - timedelta(days=i)).strftime('%d.%m.%Y')}" for i in range(num_days)]

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
