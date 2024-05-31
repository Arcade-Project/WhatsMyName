from concurrent.futures import ThreadPoolExecutor
from .requests_check import requests_check


def exec_concurrent_uri_checks(uri_checks, username, session):
    # Use ThreadPoolExecutor for concurrent execution
    with ThreadPoolExecutor(max_workers=60) as executor:
        futures = []
        for site in uri_checks:
            url = site.get("uri_check")
            e_string = site.get("e_string")
            m_string = site.get("m_string")

            e_code = site.get("e_code")
            m_code = site.get("m_code")

            name = site.get("name")

            formatted_url = url.format(account=username)

            # Submit the requests_check function to the executor
            futures.append(
                executor.submit(
                    requests_check,
                    e_string,
                    m_string,
                    formatted_url,
                    e_code,
                    m_code,
                    name,
                    session,
                )
            )
