from flask import Flask, jsonify
from urllib.parse import urljoin, urlparse, unquote
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def is_internal(base, target):
    try:
        return urlparse(base).netloc == urlparse(target).netloc
    except:
        return False

def crawl(base_url):
    visited = set()
    to_visit = [base_url]
    collected = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        while to_visit:
            url = to_visit.pop(0)
            if url in visited:
                continue

            visited.add(url)
            collected.append(url)

            try:
                page = context.new_page()
                page.goto(url, wait_until='domcontentloaded', timeout=20000)

                anchors = page.eval_on_selector_all("a[href]", "elements => elements.map(el => el.href)")

                for link in anchors:
                    normalized = urljoin(url, link).split('#')[0]
                    if is_internal(base_url, normalized) and normalized not in visited and normalized not in to_visit:
                        to_visit.append(normalized)

                page.close()
            except Exception as e:
                print(f"❌ Failed to crawl {url}: {e}")
                continue

        browser.close()

    return collected

@app.route('/crawl/<path:url>', methods=['GET'])
def crawl_endpoint(url):
    target_url = unquote(url)
    try:
        urls = crawl(target_url)
        return jsonify({
            "status": "success",
            "total": len(urls),
            "urls": urls
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
