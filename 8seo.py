import re
from collections import Counter

def keyword_stuffing_detector(text, keyword):
    """Detect keyword stuffing in text"""
    words = text.lower().split()
    keyword_count = words.count(keyword.lower())
    total_words = len(words)
    
    keyword_density = (keyword_count / total_words) * 100
    
    print(f"Keyword: {keyword}")
    print(f"Keyword count: {keyword_count}")
    print(f"Total words: {total_words}")
    print(f"Keyword density: {keyword_density:.2f}%")
    
    if keyword_density > 5:
        print("WARNING: Possible keyword stuffing detected!")
    elif keyword_density > 2:
        print("CAUTION: High keyword density")
    else:
        print("Keyword density is within acceptable range")

def generate_keyword_stuffed_content(keyword, target_density=10):
    """Generate content with keyword stuffing (for demonstration)"""
    base_content = f"Welcome to our website about {keyword}. "
    
    # Calculate how many times to repeat keyword
    base_words = len(base_content.split())
    target_keyword_count = int((target_density / 100) * base_words / (1 - target_density / 100))
    
    stuffed_content = base_content
    for i in range(target_keyword_count):
        stuffed_content += f"{keyword} "
    
    stuffed_content += f"is very important. {keyword} helps you find the best {keyword} solutions."
    
    return stuffed_content

def detect_hidden_text(html_content):
    """Detect potential hidden text techniques"""
    hidden_patterns = [
        r'style\s*=\s*["\'].*?color\s*:\s*white.*?["\']',  # White text on white background
        r'style\s*=\s*["\'].*?display\s*:\s*none.*?["\']',  # Hidden elements
        r'style\s*=\s*["\'].*?visibility\s*:\s*hidden.*?["\']',  # Invisible elements
        r'style\s*=\s*["\'].*?font-size\s*:\s*0.*?["\']',  # Zero font size
    ]
    
    potential_hidden = []
    for pattern in hidden_patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        potential_hidden.extend(matches)
    
    return potential_hidden

def analyze_meta_tags(html_content):
    """Analyze meta tags for potential spam"""
    meta_pattern = r'<meta[^>]*name\s*=\s*["\']keywords["\'][^>]*content\s*=\s*["\']([^"\']*)["\']'
    keywords_match = re.search(meta_pattern, html_content, re.IGNORECASE)
    
    if keywords_match:
        keywords = keywords_match.group(1)
        keyword_list = [k.strip() for k in keywords.split(',')]
        
        print(f"Meta keywords found: {len(keyword_list)}")
        print(f"Keywords: {keywords}")
        
        # Check for keyword repetition
        keyword_counts = Counter(keyword_list)
        repeated_keywords = {k: v for k, v in keyword_counts.items() if v > 1}
        
        if repeated_keywords:
            print("WARNING: Repeated keywords in meta tags:")
            for keyword, count in repeated_keywords.items():
                print(f"  {keyword}: {count} times")

# Example usage
sample_text = "Python programming is essential for data science. Python helps in web development. Learn Python today!"
keyword_stuffing_detector(sample_text, "Python")

print("\n" + "="*50)
stuffed_content = generate_keyword_stuffed_content("SEO", 8)
print("Generated keyword-stuffed content:")
print(stuffed_content)
keyword_stuffing_detector(stuffed_content, "SEO")
