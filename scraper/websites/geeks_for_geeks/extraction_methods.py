def method_1(soup):
    complexity = soup.find('strong', text='Time Complexity:')
    if complexity:
        return complexity.find_parent().text
    else:
        return None


EXTRACTION_METHODS = [
    method_1
]
