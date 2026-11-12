import re
import pandas as pd
from datetime import datetime
from collections import Counter

# Sample log entries
log_data = [
    '192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326 "-" "Mozilla/5.0"',
    '192.168.1.2 - - [10/Oct/2023:13:55:37 +0000] "GET /products.html HTTP/1.1" 200 5432 "http://example.com/index.html" "Mozilla/5.0"',
    '192.168.1.1 - - [10/Oct/2023:13:55:38 +0000] "GET /cart.html HTTP/1.1" 200 1234 "http://example.com/products.html" "Mozilla/5.0"',
    '192.168.1.3 - - [10/Oct/2023:13:55:39 +0000] "GET /contact.html HTTP/1.1" 404 512 "-" "Mozilla/5.0"'
]

def parse_log_line(line):
    pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'
    match = re.match(pattern, line)
    
    if match:
        return {
            'ip': match.group(1),
            'timestamp': match.group(2),
            'request': match.group(3),
            'status': int(match.group(4)),
            'size': int(match.group(5)),
            'referrer': match.group(6),
            'user_agent': match.group(7)
        }
    return None

def analyze_web_logs(log_entries):
    parsed_logs = []
    
    for entry in log_entries:
        parsed = parse_log_line(entry)
        if parsed:
            # Extract URL from request
            request_parts = parsed['request'].split()
            if len(request_parts) >= 2:
                parsed['url'] = request_parts[1]
                parsed['method'] = request_parts[0]
            parsed_logs.append(parsed)
    
    df = pd.DataFrame(parsed_logs)
    
    # Basic analytics
    print("=== Web Usage Analytics ===")
    print(f"Total requests: {len(df)}")
    print(f"Unique visitors: {df['ip'].nunique()}")
    print(f"Most visited pages:")
    print(df['url'].value_counts().head())
    print(f"\nStatus code distribution:")
    print(df['status'].value_counts())
    
    # Page views by IP
    print(f"\nPage views by IP:")
    print(df.groupby('ip')['url'].count().sort_values(ascending=False))
    
    return df

# Analyze logs
df = analyze_web_logs(log_data)
