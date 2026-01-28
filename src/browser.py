from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from playwright.sync_api import sync_playwright, Page, BrowserContext, ElementHandle


@dataclass
class Candidate:
    id: str
    text: str
    tag: str
    hint: str


class Browser:
    def __init__(self, user_data_dir: str, headless: bool = False):
        self._pw = sync_playwright().start()
        self._context: BrowserContext = self._pw.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=headless,
            viewport={"width": 1280, "height": 800},
        )
        self._page: Page = self._context.pages[0] if self._context.pages else self._context.new_page()

        # candidate_id -> ElementHandle
        self._candidate_handles: Dict[str, ElementHandle] = {}

    @property
    def page(self) -> Page:
        return self._page

    def close(self):
        try:
            self._context.close()
        finally:
            self._pw.stop()

    def goto(self, url: str) -> str:
        self._page.goto(url, wait_until="domcontentloaded")
        return f"Navigated to {url}"

    def wait(self, ms: int) -> str:
        self._page.wait_for_timeout(ms)
        return f"Waited {ms}ms"

    def press(self, key: str) -> str:
        self._page.keyboard.press(key)
        return f"Pressed {key}"

    def type_text(self, selector: str, text: str, clear: bool = False) -> str:
        loc = self._page.locator(selector).first
        loc.wait_for(state="visible", timeout=15000)
        loc.click(timeout=15000)
        if clear:
            loc.fill("")
        loc.type(text, delay=10)
        return f"Typed text into {selector}"

    def snapshot(self, max_candidates: int = 40) -> Dict[str, Any]:
        self._candidate_handles.clear()

        selectors = [
            "a[href]",
            "button",
            "input[type=button]",
            "input[type=submit]",
            "[role=button]",
            "[onclick]",
        ]
        elems: List[ElementHandle] = []
        for sel in selectors:
            try:
                elems.extend(self._page.query_selector_all(sel))
            except Exception:
                pass

        # Фильтрация
        uniq: List[ElementHandle] = []
        seen = set()
        for el in elems:
            try:
                box = el.bounding_box()
                if not box:
                    continue
                if box["width"] < 10 or box["height"] < 10:
                    continue
                key = (round(box["x"]), round(box["y"]), round(box["width"]), round(box["height"]))
                if key in seen:
                    continue
                seen.add(key)
                uniq.append(el)
            except Exception:
                continue

        candidates: List[Dict[str, str]] = []
        for i, el in enumerate(uniq[:max_candidates]):
            cid = f"c{i}"
            self._candidate_handles[cid] = el
            text = ""
            tag = ""
            hint = ""
            try:
                tag = (el.evaluate("e => e.tagName") or "").lower()
                text = (el.inner_text() or "").strip()
                if not text:
                    text = (el.get_attribute("aria-label") or "").strip()
                if not text:
                    text = (el.get_attribute("title") or "").strip()
                if not text:
                    text = (el.get_attribute("placeholder") or "").strip()

                hint = (el.get_attribute("href") or "").strip()
            except Exception:
                pass

            if not text:
                text = f"<{tag or 'element'}>"

            candidates.append(
                {"candidate_id": cid, "text": text[:120], "tag": tag[:30], "hint": hint[:120]}
            )

        return {
            "url": self._page.url,
            "title": self._page.title(),
            "candidates": candidates,
        }

    def click_candidate(self, candidate_id: str) -> str:
        el = self._candidate_handles.get(candidate_id)
        if not el:
            return f"Candidate {candidate_id} not found. Take a new snapshot."

        try:
            el.scroll_into_view_if_needed(timeout=5000)
        except Exception:
            pass

        # обычный click
        try:
            el.click(timeout=5000)
            return f"Clicked {candidate_id}"
        except Exception:
            pass

        # force click
        try:
            el.click(timeout=5000, force=True)
            return f"Clicked {candidate_id} (force)"
        except Exception:
            pass

        # координатный клик по центру
        try:
            box = el.bounding_box()
            if not box:
                raise RuntimeError("No bounding box")
            x = box["x"] + box["width"] / 2
            y = box["y"] + box["height"] / 2
            self._page.mouse.click(x, y)
            return f"Clicked {candidate_id} (mouse)"
        except Exception as e:
            return f"Failed to click {candidate_id}: {e}"
