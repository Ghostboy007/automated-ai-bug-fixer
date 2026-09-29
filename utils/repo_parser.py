def extract_code(response):

    if "---BEGIN CODE---" in response and "---END CODE---" in response:

        code = response.split(
            "---BEGIN CODE---"
        )[1].split(
            "---END CODE---"
        )[0]

        return code.strip()

    return response.strip()