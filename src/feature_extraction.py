import re
from urllib.parse import urlparse
import pandas as pd

COMMON_TWO_PART_TLDS = {
    "co.uk", "com.br", "co.id", "co.jp", "com.au", "co.nz",
    "co.za", "com.mx", "co.in", "org.uk", "net.au", "gov.uk",
}

def _get_hostname(url: str) -> str:
    if not isinstance(url, str) or url == "":
        return ""
    candidate = url if re.match(r"^https?://", url, re.IGNORECASE) else f"http://{url}"
    try:
        netloc = urlparse(candidate).netloc
        return netloc.split(":")[0]
    except ValueError:
        return ""

def url_length(url: str) -> int:
    return len(url) if isinstance(url, str) else 0

def dot_count(url: str) -> int:
    return url.count(".") if isinstance(url, str) else 0

def digit_count(url: str) -> int:
    return sum(c.isdigit() for c in url) if isinstance(url, str) else 0

def hyphen_count(url: str) -> int:
    return url.count("-") if isinstance(url, str) else 0

def special_char_count(url: str) -> int:
    if not isinstance(url, str):
        return 0
    return len(re.findall(r"[^a-zA-Z0-9./]", url))

def has_at_symbol(url: str) -> int:
    return int("@" in url) if isinstance(url, str) else 0

def subdomain_count(url: str) -> int:
    hostname = _get_hostname(url)
    if not hostname:
        return 0
    parts = hostname.split(".")
    two_part = ".".join(parts[-2:]) if len(parts) >= 2 else ""
    if two_part in COMMON_TWO_PART_TLDS and len(parts) >= 3:
        core_parts = parts[:-2]
    else:
        core_parts = parts[:-1] if len(parts) >= 2 else parts
    return max(0, len(core_parts) - 1)

def has_ip_address(url: str) -> int:
    hostname = _get_hostname(url)
    if not re.fullmatch(r"(\d{1,3}\.){3}\d{1,3}", hostname):
        return 0
    return int(all(0 <= int(octet) <= 255 for octet in hostname.split(".")))

def extract_features(df: pd.DataFrame, url_col: str = "URL") -> pd.DataFrame:
    result = pd.DataFrame(index=df.index)
    result["url_length"] = df[url_col].apply(url_length)
    result["dot_count"] = df[url_col].apply(dot_count)
    result["digit_count"] = df[url_col].apply(digit_count)
    result["hyphen_count"] = df[url_col].apply(hyphen_count)
    result["special_char_count"] = df[url_col].apply(special_char_count)
    result["has_at_symbol"] = df[url_col].apply(has_at_symbol)
    result["subdomain_count"] = df[url_col].apply(subdomain_count)
    result["has_ip_address"] = df[url_col].apply(has_ip_address)
    return result