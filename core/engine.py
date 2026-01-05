from modules import subdomains

def run(domain, mode, options):
    results = {}

    # FAST mode
    if mode == "fast":
        results["subs"] = subdomains.run(
            domain,
            passive=True,
            brute=False,
            live=True
        )
        return results

    # DEEP mode
    if mode == "deep":
        results["subs"] = subdomains.run(
            domain,
            passive=True,
            brute=True,
            live=True
        )
        return results

    # SMART mode
    if mode == "smart":
        results["subs"] = subdomains.run(
            domain,
            passive=True,
            brute=False,
            live=True
        )

        # If few subs found, escalate to brute-force
        if os.path.getsize(results["subs"]["all"]) < 200:
            results["subs"] = subdomains.run(
                domain,
                passive=True,
                brute=True,
                live=True
            )

        return results
