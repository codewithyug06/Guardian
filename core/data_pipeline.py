import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_recent_cves(vendor_name, max_results=3):
    """
    Fetches recent CVEs related to a vendor.
    In a full production environment, this would hit the NVD API with an API key.
    Here we try a public query and fallback to synthetic data if rate-limited.
    """
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={vendor_name}&resultsPerPage={max_results}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            cves = []
            for item in data.get("vulnerabilities", []):
                cve_id = item.get("cve", {}).get("id", "Unknown ID")
                desc = "Unknown Description"
                for d in item.get("cve", {}).get("descriptions", []):
                    if d.get("lang") == "en":
                        desc = d.get("value")
                        break
                
                # Basic severity check
                metrics = item.get("cve", {}).get("metrics", {})
                severity = "MEDIUM"
                if "cvssMetricV31" in metrics:
                    severity = metrics["cvssMetricV31"][0].get("cvssData", {}).get("baseSeverity", "MEDIUM")
                
                cves.append({
                    "id": cve_id,
                    "description": desc,
                    "severity": severity
                })
            return cves
        else:
            logger.warning(f"NVD API returned status code {response.status_code}. Using fallback.")
            return _generate_fallback_cve(vendor_name)
    except Exception as e:
        logger.error(f"Error fetching CVEs for {vendor_name}: {str(e)}. Using fallback.")
        return _generate_fallback_cve(vendor_name)

def _generate_fallback_cve(vendor_name):
    """Fallback generator if external API is unreachable or rate-limited."""
    return [
        {
            "id": f"CVE-2026-{hash(vendor_name) % 10000:04d}",
            "description": f"A simulated vulnerability was found in {vendor_name} affecting recent API endpoints.",
            "severity": "HIGH"
        }
    ]

def scan_vendor_supply_chain(vendor_list=["AWS", "Stripe", "Auth0"]):
    """Scans a list of vendors for active supply chain risks."""
    alerts = []
    for vendor in vendor_list:
        cves = fetch_recent_cves(vendor, max_results=1)
        for cve in cves:
            if cve["severity"] in ["HIGH", "CRITICAL"]:
                alerts.append(f"🚨 VENDOR CRITICAL ({vendor}): {cve['id']} - {cve['description'][:100]}...")
            else:
                alerts.append(f"⚠️ VENDOR ALERT ({vendor}): {cve['id']} - {cve['severity']} severity detected.")
    
    if not alerts:
        return ["✅ SUPPLY CHAIN: All vendor security profiles nominal."]
    return alerts
