
import re
from collections import Counter
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was",
    "were", "to", "of", "in", "on", "for", "with", "by", "as",
    "at", "from", "it", "this", "that", "be", "has", "have",
    "had", "you", "your", "our", "we", "they", "their", "he",
    "she", "his", "her", "if", "can", "will", "all", "across",
    "who", "what", "how", "do", "does", "not", "both", "into"
}


def fetch_website(url):
    """Fetch a public website and return its HTML."""
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Enter a valid HTTP or HTTPS URL.")

    response = requests.get(
        url,
        timeout=20,
        headers={"User-Agent": "SEO-Audit-Tool/1.0"},
        allow_redirects=True
    )
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if "html" not in content_type.lower():
        raise ValueError("The URL did not return an HTML page.")

    return response.text, response.url, response.status_code


def get_visible_text(soup):
    """Extract text while excluding non-visible/code elements."""
    copy_soup = BeautifulSoup(str(soup), "html.parser")

    for tag in copy_soup.find_all(
        ["script", "style", "noscript", "template", "svg"]
    ):
        tag.decompose()

    return copy_soup.get_text(" ", strip=True)


def keyword_stuffing_detector(text, keyword):
    """Measure exact phrase occurrences and approximate density."""
    words = re.findall(r"\b[\w'-]+\b", text.lower())
    keyword_words = re.findall(r"\b[\w'-]+\b", keyword.lower())

    if not words:
        print("No readable page text found.")
        return

    if not keyword_words:
        print("No keyword entered.")
        return

    # Match the complete phrase, ignoring case and extra whitespace.
    phrase = r"\s+".join(re.escape(w) for w in keyword_words)
    occurrences = list(re.finditer(
        r"(?<!\w)" + phrase + r"(?!\w)",
        text,
        re.IGNORECASE
    ))

    count = len(occurrences)
    total_words = len(words)

    # Density counts the words in each phrase occurrence.
    density = (count * len(keyword_words) / total_words) * 100

    print(f"\nKeyword/phrase: {keyword}")
    print(f"Occurrences: {count}")
    print(f"Total words: {total_words}")
    print(f"Approximate keyword density: {density:.2f}%")

    if density > 5:
        print("WARNING: High keyword density; review manually.")
    elif density > 2:
        print("CAUTION: Check whether repetition is natural.")
    else:
        print("No high-density warning from this threshold.")

    print("Note: Density thresholds are heuristics, not Google rules.")


def analyze_repeated_words(text):
    """Report frequently repeated meaningful words."""
    words = re.findall(r"\b[a-z][a-z'-]{2,}\b", text.lower())
    counts = Counter(w for w in words if w not in STOP_WORDS)

    print("\n=== Most Frequent Meaningful Words ===")
    for word, count in counts.most_common(15):
        print(f"{word}: {count}")


def detect_hidden_text(soup):
    """Flag suspicious inline CSS patterns for manual review."""
    patterns = {
        "display:none": r"display\s*:\s*none\b",
        "visibility:hidden": r"visibility\s*:\s*hidden\b",
        "zero font size": r"font-size\s*:\s*0(?:px|em|rem|%)?\b",
        "white text": r"color\s*:\s*(?:white\b|#fff(?:fff)?\b|rgb\(\s*255\s*,\s*255\s*,\s*255\s*\))",
    }

    findings = []

    for tag in soup.find_all(style=True):
        style = tag.get("style", "")
        for label, pattern in patterns.items():
            if re.search(pattern, style, re.IGNORECASE):
                findings.append({
                    "pattern": label,
                    "tag": tag.name,
                    "style": style[:180]
                })

    print("\n=== Potential Hidden Text Indicators ===")

    if not findings:
        print("No matching inline CSS patterns found.")
    else:
        for item in findings:
            print(
                f"- {item['pattern']} | "
                f"<{item['tag']}> | {item['style']}"
            )

    print("These are indicators, not proof of deceptive hidden text.")


def analyze_meta_tags(soup):
    """Inspect title, description, and repeated meta keywords."""
    print("\n=== SEO Metadata ===")

    title_tag = soup.find("title")
    title = title_tag.get_text(" ", strip=True) if title_tag else ""

    description_tag = soup.find(
        "meta", attrs={"name": re.compile(r"^description$", re.I)}
    )
    description = (
        description_tag.get("content", "").strip()
        if description_tag else ""
    )

    keywords_tag = soup.find(
        "meta", attrs={"name": re.compile(r"^keywords$", re.I)}
    )
    keywords = keywords_tag.get("content", "") if keywords_tag else ""

    print(f"Title: {title or '[Missing]'}")
    print(f"Title length: {len(title)} characters")
    print(f"Meta description: {description or '[Missing]'}")
    print(f"Description length: {len(description)} characters")

    if not keywords:
        print("Meta keywords tag: Not present")
        return

    keyword_list = [
        item.strip().lower()
        for item in keywords.split(",")
        if item.strip()
    ]
    counts = Counter(keyword_list)
    repeated = {k: v for k, v in counts.items() if v > 1}

    print(f"Meta keywords: {keywords}")
    print(f"Number of keyword entries: {len(keyword_list)}")

    if repeated:
        print("Repeated meta keywords:")
        for word, count in repeated.items():
            print(f"- {word}: {count} times")
    else:
        print("No duplicate meta keyword entries.")

    print("Meta keywords are not a meaningful Google ranking signal.")


def analyze_website(url, target_keyword):
    html, final_url, status = fetch_website(url)
    soup = BeautifulSoup(html, "html.parser")
    text = get_visible_text(soup)

    print("\n" + "=" * 55)
    print("WEBSITE SEO SPAM SCREENING REPORT")
    print("=" * 55)
    print(f"Requested URL: {url}")
    print(f"Final URL: {final_url}")
    print(f"HTTP status: {status}")
    print(f"HTML title: {soup.title.get_text(strip=True) if soup.title else '[Missing]'}")
    print(f"Visible word count: {len(text.split())}")

    analyze_meta_tags(soup)
    keyword_stuffing_detector(text, target_keyword)
    analyze_repeated_words(text)
    detect_hidden_text(soup)

    print("\n=== Audit Limitations ===")
    print("- Only the fetched page is analyzed.")
    print("- JavaScript-rendered text may be missed.")
    print("- External CSS and computed visibility are not evaluated.")
    print("- Repeated words can be natural in legal/service pages.")
    print("- Review flagged content before concluding it is spam.")
    print("=" * 55)


if __name__ == "__main__":
    url = input(
        "Enter website URL [https://rupeshmittal.in]: "
    ).strip() or "https://rupeshmittal.in"

    keyword = input(
        "Enter target keyword/phrase "
        "[cyber lawyer in Hyderabad]: "
    ).strip() or "cyber lawyer in Hyderabad"

    try:
        analyze_website(url, keyword)
    except requests.RequestException as error:
        print(f"Website request failed: {error}")
    except (ValueError, Exception) as error:
        print(f"Analysis failed: {error}")
