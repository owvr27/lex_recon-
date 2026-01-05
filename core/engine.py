from modules import subdomains, urls, js, params

def run(domain, mode, options):
    results = {}

    # FAST
    if mode == "fast":
        results["subs"] = subdomains.run(domain, passive=True)
        results["urls"] = urls.run(domain, archive_only=True)
        return results

    # DEEP
    if mode == "deep":
        results["subs"] = subdomains.run(domain, passive=True, live=True)
        results["urls"] = urls.run(domain)
        results["js"] = js.run(domain)
        results["params"] = params.run(domain)
        return results

    # SMART
    if mode == "smart":
        results["subs"] = subdomains.run(domain, passive=True)
        results["urls"] = urls.run(domain, archive_only=True)

        # decision logic
        if urls.has_js(domain):
            results["js"] = js.run(domain)

        if urls.has_params(domain):
            results["params"] = params.run(domain)

        return results
