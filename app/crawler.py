import asyncio
import json
import logging
from datetime import datetime
from urllib.parse import urljoin, urlparse

import aiohttp
import tldextract
from bs4 import BeautifulSoup
from flask import Flask, request, Response, render_template
from flasgger import Swagger
from sqlalchemy.dialects.postgresql import insert

from models import db, Page

# Flask App
app = Flask(__name__)
Swagger(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db:5432/crawler_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Глобальные переменные
visited = set()
site_structure = {}

with app.app_context():
    db.create_all()

# Базовые селекторы
default_selectors = {
    'wordpress': {
        'header': ['header', 'div[class*="site-header"]', 'div[class*="header"]'],
        'footer': ['footer', 'div[class*="site-footer"]', 'div[class*="footer"]']
    },
    'tilda': {
        'header': ['div.t228', 'div.t-header'],
        'footer': ['div.t-footer', 'div.t948']
    },
    'bitrix': {
        'header': ['div[class*="header"]', 'div[id*="header"]'],
        'footer': ['div[class*="footer"]', 'div[id*="footer"]']
    },
    'html5': {
        'header': ['header'],
        'footer': ['footer']
    }
}


async def save_page(page_data):
    stmt = insert(Page).values(
        url=page_data["url"],
        header_found=page_data["header_found"],
        footer_found=page_data["footer_found"],
        header_selector=page_data["header_selector"],
        footer_selector=page_data["footer_selector"],
        created_at=page_data["created_at"],
        links=page_data["links"],
        is_media=page_data["is_media"],
        title=page_data.get("title"),
        meta_description=page_data.get("meta_description"),
        content=page_data.get("content"),
        image_urls=page_data.get("image_urls"),
        published_date=page_data.get("published_date"),
    )

    stmt = stmt.on_conflict_do_update(
        index_elements=["url"],
        set_={
            "header_found": stmt.excluded.header_found,
            "footer_found": stmt.excluded.footer_found,
            "header_selector": stmt.excluded.header_selector,
            "footer_selector": stmt.excluded.footer_selector,
            "updated_at": stmt.excluded.created_at,
            "links": stmt.excluded.links,
            "is_media": stmt.excluded.is_media,
            "title": stmt.excluded.title,
            "meta_description": stmt.excluded.meta_description,
            "content": stmt.excluded.content,
            "image_urls": stmt.excluded.image_urls,
            "published_date": stmt.excluded.published_date,
        }
    )

    db.session.execute(stmt)
    db.session.commit()


def is_internal_link(link, domain):
    parsed = urlparse(link)
    return (not parsed.netloc or domain in parsed.netloc) and parsed.scheme in ("http", "https", "")


def extract_blocks(soup, header_selectors, footer_selectors):
    def match_selector(selectors):
        for sel in selectors:
            el = soup.select_one(sel)
            if el:
                return el
        return None

    header = match_selector(header_selectors)
    footer = match_selector(footer_selectors)

    return {
        "header_found": bool(header),
        "footer_found": bool(footer),
        "header_selector": header.name if header else None,
        "footer_selector": footer.name if footer else None
    }


async def fetch(session, url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36"
        }
        async with session.get(url, headers=headers, timeout=10) as response:
            content_type = response.headers.get("Content-Type", "").lower()
            if "html" in content_type:
                is_media = False
                result = await response.text()
                return is_media, result
            else:
                is_media = True
                return is_media, url
    except Exception as e:
        logger.error(f"Failed to load {url}: {e}")
        return False, None


async def crawl(session, start_url, base_domain, header_selectors, footer_selectors, max_depth=2, depth=0, parsed_pages=None):
    if start_url in visited or depth > max_depth:
        return

    visited.add(start_url)
    logger.info(f"Crawling: {start_url}")

    is_media, content = await fetch(session, start_url)

    if not content:
        return

    soup = None
    blocks = {
        "header_found": False,
        "footer_found": False,
        "header_selector": None,
        "footer_selector": None
    }
    links_on_page = []

    title = None
    meta_description = None
    content_text = None
    image_urls = []
    published_date = None

    if not is_media:
        soup = BeautifulSoup(content, "lxml")
        blocks = extract_blocks(soup, header_selectors, footer_selectors)

        if soup.title:
            title = soup.title.string.strip()

        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag and meta_tag.get("content"):
            meta_description = meta_tag["content"].strip()

        if not title:
            h1_tag = soup.find("h1")
            if h1_tag:
                title = h1_tag.text.strip()

        body = soup.find("body")
        if body:
            content_text = str(body)

        for img_tag in soup.find_all("img", src=True):
            img_url = urljoin(start_url, img_tag["src"])
            image_urls.append(img_url)

        published_tag = soup.find(attrs={"itemprop": "datePublished"}) or \
                        soup.find("meta", attrs={"property": "article:published_time"}) or \
                        soup.find("time", attrs={"datetime": True})

        if published_tag:
            date_str = published_tag.get("content") or published_tag.get("datetime")
            if date_str:
                try:
                    published_date = datetime.fromisoformat(date_str)
                except Exception:
                    pass

        for link_tag in soup.find_all("a", href=True):
            link = urljoin(start_url, link_tag["href"])
            link = link.split("#")[0]
            if is_internal_link(link, base_domain) and link not in links_on_page:
                links_on_page.append(link)

    await save_page({
        "url": start_url,
        "header_found": blocks['header_found'],
        "footer_found": blocks['footer_found'],
        "header_selector": blocks['header_selector'],
        "footer_selector": blocks['footer_selector'],
        "created_at": datetime.utcnow(),
        "updated_at": None,
        "is_media": is_media,
        "links": links_on_page,
        "title": title,
        "meta_description": meta_description,
        "content": content_text,
        "image_urls": image_urls,
        "published_date": published_date
    })

    if parsed_pages is not None:
        parsed_pages.append({
            "url": start_url,
            "header_found": blocks['header_found'],
            "footer_found": blocks['footer_found'],
            "title": title,
            "meta_description": meta_description,
            "content": content_text,
            "is_media": is_media,
            "image_urls": image_urls,
            "published_date": published_date.isoformat() if published_date else None,
            "links": links_on_page
        })

    tasks = []

    for link in links_on_page:
        if link not in visited:
            tasks.append(crawl(session, link, base_domain, header_selectors, footer_selectors, max_depth, depth + 1, parsed_pages=parsed_pages))

    await asyncio.gather(*tasks)

@app.route("/crawl", methods=["GET"])
def crawl_form():
    """
    GET /crawl
    ---
    description: Возвращает HTML-форму для запуска краулинга.
    responses:
      200:
        description: Форма для запуска краулинга.
    """
    return render_template("index.html")

@app.route("/crawl", methods=["POST"])
def start_crawl():
    """
    POST /crawl
    ---
    summary: Запускает асинхронный краулинг сайта
    consumes:
      - application/json
      - application/x-www-form-urlencoded
    parameters:
      - in: body
        name: body
        description: Параметры для краулинга сайта (если отправляется как JSON)
        required: false
        schema:
          type: object
          properties:
            start_url:
              type: string
              description: URL, с которого начинается краулинг
              example: "https://example.com"
            max_depth:
              type: integer
              description: Максимальная глубина обхода ссылок
              example: 2
            type:
              type: string
              description: Тип сайта (wordpress, tilda, bitrix, html5)
              example: "wordpress"
    responses:
      200:
        description: Результаты краулинга страниц
        schema:
          type: object
          properties:
            pages:
              type: array
              items:
                type: object
                properties:
                  url:
                    type: string
                  header_found:
                    type: boolean
                  footer_found:
                    type: boolean
                  title:
                    type: string
                    nullable: true
                  meta_description:
                    type: string
                    nullable: true
                  content:
                    type: string
                    nullable: true
                  is_media:
                    type: boolean
                  image_urls:
                    type: array
                    items:
                      type: string
                  published_date:
                    type: string
                    format: date-time
                    nullable: true
                  links:
                    type: array
                    items:
                      type: string
    """
    if request.content_type == 'application/json':
        data = request.get_json()
    else:
        data = {
            "start_url": request.form["start_url"],
            "max_depth": int(request.form.get("max_depth", 2)),
            "type": request.form.get("type")
        }

    start_url = data["start_url"]
    max_depth = data.get("max_depth", 2)
    type_ = data.get("type", None)

    header_selectors = data.get("header_selectors", [])
    footer_selectors = data.get("footer_selectors", [])

    if type_ in default_selectors:
        header_selectors += default_selectors[type_]["header"]
        footer_selectors += default_selectors[type_]["footer"]

    visited.clear()

    ext = tldextract.extract(start_url)
    base_domain = f"{ext.domain}.{ext.suffix}"

    parsed_pages = []

    async def runner():
        async with aiohttp.ClientSession() as session:
            await crawl(session, start_url, base_domain, header_selectors, footer_selectors, max_depth=max_depth, parsed_pages=parsed_pages)

    asyncio.run(runner())

    return Response(json.dumps({"pages": parsed_pages}, ensure_ascii=False, indent=2),
                    content_type="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
