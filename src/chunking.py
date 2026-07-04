import re

def split_requirements(text: str) -> list:
    pattern = r'(?:^|\n)((?:REQ[-\s]?\d+|\d+\.[\d.]*|\d+\))\s*.+?)(?=\n(?:REQ[-\s]?\d+|\d+\.[\d.]*|\d+\))|$)'
    matches = re.findall(pattern, text, flags=re.DOTALL)
    reqs = [{"id": f"REQ-{i+1}", "text": m.strip()} for i, m in enumerate(matches) if len(m.strip()) > 15]
    if not reqs:
        # fallback: split by paragraphs if no numbered pattern found
        paras = [p.strip() for p in text.split("\n") if len(p.strip()) > 20]
        reqs = [{"id": f"REQ-{i+1}", "text": p} for i, p in enumerate(paras)]
    return reqs