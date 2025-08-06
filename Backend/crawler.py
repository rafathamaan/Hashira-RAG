import requests

md_urls = [
    "https://docs.garden.finance/developers/overview.md",
    "https://docs.garden.finance/developers/supported-chains.md",
    "https://docs.garden.finance/developers/supported-routes.md",
    "https://docs.garden.finance/developers/affiliate-fees.md",
    "https://docs.garden.finance/developers/api/overview.md",
    "https://docs.garden.finance/developers/api/1click.md",
    "https://docs.garden.finance/developers/sdk/overview.md",
    "https://docs.garden.finance/developers/sdk/react/quickstart.md",
    "https://docs.garden.finance/developers/sdk/react/setup.md",
    "https://docs.garden.finance/developers/sdk/nodejs/quickstart.md",
    "https://docs.garden.finance/developers/sdk/nodejs/setup.md",
    "https://docs.garden.finance/developers/core/order-lifecycle.md",
    "https://docs.garden.finance/developers/core/sessions.md",
    "https://docs.garden.finance/developers/guides/cookbook.md",
    "https://docs.garden.finance/developers/guides/sdk.md",
    "https://docs.garden.finance/developers/localnet.md"
]

output_file = "total_docs.md"

with open(output_file, "w", encoding="utf-8") as f:
    for url in md_urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                content = response.text
                f.write(f"\n\n--- Content from {url} ---\n\n")
                f.write(content)
                print(f"Saved content from {url} ({len(content)} characters)")
            else:
                print(f"Failed to fetch {url}, status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")

print(f"All docs saved to {output_file}")
