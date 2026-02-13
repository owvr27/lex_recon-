from core.utils import count_lines

def build_report(domain, results, output_dir):
    report = {
        "target": domain,
        "summary": {}
    }

    if "subs" in results:
        report["summary"]["subdomains_total"] = count_lines(results["subs"]["all"])
        report["summary"]["subdomains_live"] = count_lines(results["subs"]["live"])

    if "urls" in results:
        report["summary"]["urls_total"] = count_lines(results["urls"]["all"])

    if "js" in results:
        report["summary"]["js_endpoints"] = count_lines(results["js"]["all"])

    if "params" in results:
        report["summary"]["parameters"] = count_lines(results["params"]["all"])

    return report
