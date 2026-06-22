import os
import re
import json
import urllib.request
import urllib.parse

def clean_url(url):
    url = url.strip().strip("'").strip('"')
    parsed = urllib.parse.urlparse(url)
    return url, parsed

def download_file(url, local_path):
    print(f"Downloading {url} -> {local_path}")
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req) as response:
            data = response.read()
        with open(local_path, 'wb') as out_file:
            out_file.write(data)
        return data
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def process_css_for_urls(css_data, css_url, local_css_path, root_dir):
    try:
        css_text = css_data.decode('utf-8', errors='ignore')
    except Exception:
        return
    
    # Regex to find url(...)
    matches = re.findall(r'url\((.*?)\)', css_text)
    
    for match in matches:
        raw_url = match.strip().strip("'").strip('"')
        if not raw_url or raw_url.startswith('data:') or raw_url.startswith('http://') or raw_url.startswith('https://') or raw_url.startswith('//'):
            continue
        
        # It's a relative URL, resolve it relative to css_url
        absolute_asset_url = urllib.parse.urljoin(css_url, raw_url)
        
        # Calculate local path relative to local_css_path
        clean_raw_url = raw_url.split('?')[0].split('#')[0]
        css_dir = os.path.dirname(local_css_path)
        local_asset_path = os.path.abspath(os.path.join(css_dir, clean_raw_url))
        
        # Ensure the local path is within root_dir
        if local_asset_path.startswith(root_dir):
            download_file(absolute_asset_url, local_asset_path)

def main():
    root_dir = r"C:\Users\AVINASH KUMAR\Documents\icai"
    os.makedirs(root_dir, exist_ok=True)
    
    # Read the step output file which has JSON string of HTML
    step_output_file = r"C:\Users\AVINASH KUMAR\.gemini\antigravity-cli\brain\b08314c1-0084-4efb-b731-e2ab01f8c427\.system_generated\steps\70\output.txt"
    with open(step_output_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract JSON string
    start_idx = content.find('"')
    if start_idx == -1:
        print("Failed to find JSON start in output.txt")
        return
    
    # The JSON string ends before the "Ran Playwright code" section
    end_idx = content.find('"\n### Ran Playwright code')
    if end_idx == -1:
        # Fallback to finding the next double quote at the end of a line
        end_idx = content.find('"\n')
        
    if end_idx == -1:
        print("Failed to find JSON end in output.txt")
        return
        
    json_str = content[start_idx : end_idx + 1]
    try:
        html_content = json.loads(json_str)
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        return
    
    # Lists of known resources
    css_urls = [
        "https://fonts.googleapis.com/css?family=Roboto",
        "https://cdnicai.s3.ap-south-1.amazonaws.com/bootstrap/css/bootstrap.min.css",
        "https://cdnicai.s3.ap-south-1.amazonaws.com/fonts/font-awesome/css/font-awesome.min.css",
        "https://cdnicai.s3.ap-south-1.amazonaws.com/css/style.css"
    ]
    
    js_urls = [
        "https://cdnicai.s3.ap-south-1.amazonaws.com/js/jquery.min.js",
        "https://cdnicai.s3.ap-south-1.amazonaws.com/bootstrap/js/bootstrap.min.js"
    ]
    
    img_urls = [
        "https://cdnicai.s3.ap-south-1.amazonaws.com/images/moblogo.png",
        "https://cdnicai.s3.ap-south-1.amazonaws.com/images/New%20folder/logo-icai1.png",
        "https://cdnicai.s3.ap-south-1.amazonaws.com/images/telegram-icai2.png",
        "https://resource.cdn.icai.org/75238icaithreads.jpg",
        "https://resource.cdn.icai.org/76207twitternewlogo.jpg",
        "https://resource.cdn.icai.org/76211icaiwhatsapp.jpg",
        "https://cdnicai.s3.ap-south-1.amazonaws.com/images/favicon.ico"
    ]
    
    # We will map each downloaded URL to its local path
    url_to_local_path = {}
    
    # Process CSS
    for url in css_urls:
        _, parsed = clean_url(url)
        if "fonts.googleapis.com" in parsed.netloc:
            # For Google Fonts, keep it remote
            url_to_local_path[url] = url
            continue
        
        rel_path = parsed.path.lstrip('/')
        rel_path = urllib.parse.unquote(rel_path)
        local_path = os.path.join(root_dir, rel_path)
        
        css_data = download_file(url, local_path)
        if css_data:
            url_to_local_path[url] = rel_path
            process_css_for_urls(css_data, url, local_path, root_dir)
            
    # Process JS
    for url in js_urls:
        _, parsed = clean_url(url)
        rel_path = parsed.path.lstrip('/')
        rel_path = urllib.parse.unquote(rel_path)
        local_path = os.path.join(root_dir, rel_path)
        js_data = download_file(url, local_path)
        if js_data:
            url_to_local_path[url] = rel_path
            
    # Process Images
    for url in img_urls:
        _, parsed = clean_url(url)
        if "resource.cdn.icai.org" in parsed.netloc:
            rel_path = "resource/" + parsed.path.lstrip('/')
        else:
            rel_path = parsed.path.lstrip('/')
        rel_path = urllib.parse.unquote(rel_path)
        local_path = os.path.join(root_dir, rel_path)
        img_data = download_file(url, local_path)
        if img_data:
            url_to_local_path[url] = rel_path

    # Rewrite HTML references
    modified_html = html_content
    
    # 1. Remove base tag
    modified_html = re.sub(r'<base\s+href="[^"]*"\s*\/?>', '', modified_html, flags=re.IGNORECASE)
    
    # 2. Replace URLs
    for remote_url, local_rel in url_to_local_path.items():
        modified_html = modified_html.replace(remote_url, local_rel)
        modified_html = modified_html.replace(urllib.parse.quote(remote_url, safe=':/'), local_rel)
        
    # 3. Rewrite relative links to point to the live website
    modified_html = re.sub(r'href="/([^/])', r'href="https://www.icai.org/\1', modified_html)
    modified_html = re.sub(r'src="/([^/])', r'src="https://www.icai.org/\1', modified_html)
    modified_html = modified_html.replace('href="/"', 'href="https://www.icai.org/"')

    # Write updated HTML
    dest_html_file = os.path.join(root_dir, "index.html")
    with open(dest_html_file, 'w', encoding='utf-8') as f:
        f.write(modified_html)
    print(f"Clone complete! Saved to {dest_html_file}")

if __name__ == "__main__":
    main()
