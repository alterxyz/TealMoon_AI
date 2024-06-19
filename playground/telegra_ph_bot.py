# https://telegra.ph/api

import requests
import json


class TelegraphAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.telegra.ph"

        # Get account info on initialization
        account_info = self.get_account_info()
        self.short_name = account_info.get("short_name")
        self.author_name = account_info.get("author_name")
        self.author_url = account_info.get("author_url")

    def create_page(self, title, content, author_name=None, author_url=None, return_content=False):
        """
        Creates a new Telegraph page.

        Args:
            title (str): Page title (1-256 characters).
            content (list): Content of the page as a list of Node dictionaries.
            author_name (str, optional): Author name (0-128 characters). Defaults to account's author_name.
            author_url (str, optional): Profile link (0-512 characters). Defaults to account's author_url.
            return_content (bool, optional): If True, return the content field in the response.

        Returns:
            str: URL of the created page.

        Raises:
            requests.exceptions.RequestException: If the request fails.

        
        """
        url = f"{self.base_url}/createPage"
        data = {
            "access_token": self.access_token,
            "title": title,
            "content": json.dumps(content),
            "return_content": return_content,
            # Use provided author info or fall back to account info
            "author_name": author_name if author_name else self.author_name,
            "author_url": author_url if author_url else self.author_url,
        }

        response = requests.post(url, data=data)
        response.raise_for_status()
        response = response.json()
        '''
        {
            "ok": true,
            "result": {
                "path": "test-3-06-19-2",
                "url": "https://telegra.ph/test-3-06-19-2",
                "title": "test-3",
                "description": "",
                "author_name": "TealMoon",
                "author_url": "https://t.me/TealMoon_Rin",
                "views": 0,
                "can_edit": true
            }
        }
        '''
        page_url = response["result"]["url"]
        return page_url

    def get_account_info(self):
        """
        Gets information about the Telegraph account.

        Returns:
            dict: Account information including short_name, author_name, and author_url.
                 Returns None if there's an error.
        """
        url = f"{self.base_url}/getAccountInfo?access_token={self.access_token}"  # &fields=[\"author_name\",\"author_url\"] for specific fields
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()["result"]
        else:
            print(f"Fail getting telegra.ph token info: {response.status_code}")
            return None


# Example usage:
# Replace with your actual access token
access_token = ""
ph = TelegraphAPI(access_token)

# Let's try get page `Sample-Page-12-15`
def get_page(path):
    # Example : https://api.telegra.ph/getPage/Sample-Page-12-15?return_content=true
    url = f"https://api.telegra.ph/getPage/{path}?return_content=true"
    response = requests.get(url)
    return response.json()
path = "test-3-06-19-2"
# response = get_page(path)
# print(json.dumps(response, indent=4))

content = [
    {"tag": "p", "children": ["Hello, world!"]},
    {"tag": "p", "children": [{"tag": "br"}]},
    {"tag": "p", "children": ["一个简单普通的测试, 也是第一篇文章(with this account)"]},
    {"tag": "p", "children": [{"tag": "br"}]},
    {"tag": "p", "children": ["第三行"]},
    {"tag": "p", "children": ["第四行"]},
    {"tag": "p", "children": [{"tag": "strong", "children": ["5th"]}]},
    {"tag": "p", "children": [{"tag": "em", "children": ["6th"]}]},
    {"tag": "blockquote", "children": ["7th"]},
    {"tag": "p", "children": [{"tag": "a", "attrs": {"href": "https://www.google.com/", "target": "_blank"}, "children": ["8th"]}]},
    {"tag": "h3", "attrs": {"id": "9th"}, "children": ["9th"]},
    {"tag": "h4", "attrs": {"id": "10th"}, "children": ["10th"]},
    {"tag": "p", "children": [{"tag": "br"}]},
]

# Create a new page
response = ph.create_page("test-4", content)
print(response)



