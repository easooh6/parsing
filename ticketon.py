import requests
import json

def scratch(month, start_day=1, end_day=31):
    all_events = []
    
    for day in range(start_day, end_day + 1):
        page = 1
        day_events = []
        
        while True:
            url = f'https://ticketon.kz/api/v1/categories/concerts/events/?&lang=ru&render=react&per_page=12&page={page}&lang=ru&filter[timestamp]=2025-{month:02d}-{day:02d}'
            print(f"Fetching: {url}")
            response = requests.get(url)
            
            try:
                soup = response.json()
                if soup.get('error'):
                    print(f"No data for day {day}")
                    break
                    
                data = soup['data']['data']
                if not data:  # Empty page - move to next page or day
                    break
                    
                for event in data:
                    try:
                        current = {
                            "title": event['titleRu'],
                            "type": event['type'],
                            "date": event['date'],
                            "place": event['place'],
                            "hall": event['hall'],
                            "price": event['price']['min'],
                            "city": event['city']
                        }
                        day_events.append(current)
                    except Exception as e:
                        print(f"Error processing event: {e}")
                        
                page += 1
                
            except Exception as e:
                print(f"Error on day {day}, page {page}: {e}")
                break
                
        print(f"Day {day}: Found {len(day_events)} events")
        all_events.extend(day_events)
            
    return all_events

# Get events for May (month 5)
events = scratch(6)  # Limit to first 15 days for testing
print(f"Total events found: {len(events)}")

with open('ticketon.json','w',encoding='utf-8') as file:
    json.dump(events, file, indent=4, ensure_ascii=False)
