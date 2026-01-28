from __future__ import annotations

import json
import os
from typing import Any, Dict, List

from openai import OpenAI

from .browser import Browser
from .prompt import SYSTEM_PROMPT, DEVELOPER_PROMPT
from .tools import TOOLS


class Agent:
    def __init__(self, browser: Browser):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set (put it into .env)")

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.browser = browser

    def run(self, task: str, max_steps: int = 12) -> str:
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "developer", "content": DEVELOPER_PROMPT},
            {"role": "user", "content": task},
        ]

        for step in range(1, max_steps + 1):
            print(f"\n=== STEP {step} ===")

            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
            )

            msg = resp.choices[0].message
            tool_calls = getattr(msg, "tool_calls", None)

            if tool_calls:
                # Вызывает инструменты
                messages.append(
                    {
                        "role": "assistant",
                        "content": msg.content or "",
                        "tool_calls": tool_calls,
                    }
                )

                for call in tool_calls:
                    name = call.function.name
                    args = json.loads(call.function.arguments or "{}")

                    out = self._execute_tool(name, args)

                    # ЛОГИ
                    print(f"Using tool: {name}")
                    print("Input:")
                    print(json.dumps(args, ensure_ascii=False, indent=2))
                    print("Result:")
                    print(json.dumps(out, ensure_ascii=False, indent=2))

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": call.id,
                            "content": json.dumps(out, ensure_ascii=False),
                        }
                    )

                continue

            # Результат работы, итог
            final = msg.content or ""
            messages.append({"role": "assistant", "content": final})
            return final or "Done."

        return "Stopped: reached max_steps without completion."

    def _execute_tool(self, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if name == "browser_goto":
                return {"ok": True, "content": self.browser.goto(args["url"])}

            if name == "browser_snapshot":
                snap = self.browser.snapshot(max_candidates=int(args.get("max_candidates", 40)))
                return {"ok": True, **snap}

            if name == "browser_click":
                return {"ok": True, "content": self.browser.click_candidate(args["candidate_id"])}

            if name == "browser_press":
                return {"ok": True, "content": self.browser.press(args["key"])}

            if name == "browser_type":
                return {
                    "ok": True,
                    "content": self.browser.type_text(
                        selector=args["selector"],
                        text=args["text"],
                        clear=bool(args.get("clear", False)),
                    ),
                }

            if name == "browser_wait":
                return {"ok": True, "content": self.browser.wait(int(args["ms"]))}

            return {"ok": False, "content": f"Unknown tool: {name}"}
        except Exception as exc:
            return {"ok": False, "content": f"Tool error: {exc}"}
