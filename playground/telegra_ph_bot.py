"""
For getting the telegra.ph token with account in Telegram bot:
1. https://t.me/telegraph
2. Log in xxx on this device
3. On Browser at https://telegra.ph/, press F12 or right click and inspect
4. Go to Application -> Storage -> Cookies -> https://telegra.ph/
5. The token at `tph_token` is the token for telegra.ph API

Do not share the token with others, it's like a password.
"""

from bs4 import BeautifulSoup
import markdown
import requests
import json
import re
import markdown  # pip install Markdown
from bs4 import BeautifulSoup  # pip install beautifulsoup4

access_token = ""


class TelegraphAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.telegra.ph"

        # Get account info on initialization
        account_info = self.get_account_info()
        self.short_name = account_info.get("short_name")
        self.author_name = account_info.get("author_name")
        self.author_url = account_info.get("author_url")

    def create_page(
        self, title, content, author_name=None, author_url=None, return_content=False
    ):
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

    def edit_page(
        self,
        path,
        title,
        content,
        author_name=None,
        author_url=None,
        return_content=False,
    ):
        """
        Edits an existing Telegraph page.

        Args:
            path (str): Path of the page to edit.
            title (str): New page title (1-256 characters).
            content (list): New content of the page as a list of Node dictionaries.
            author_name (str, optional): Author name (0-128 characters). Defaults to account's author_name.
            author_url (str, optional): Profile link (0-512 characters). Defaults to account's author_url.
            return_content (bool, optional): If True, return the content field in the response.

        Returns:
            str: URL of the edited page.

        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        url = f"{self.base_url}/editPage"
        data = {
            "access_token": self.access_token,
            "path": path,
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

        page_url = response["result"]["url"]
        return page_url

    def get_page(self, path):
        """
        Gets information about a Telegraph page.

        Args:
            path (str): Path of the page to get.

        Returns:
            dict: Information about the page.
        """
        url = f"{self.base_url}/getPage/{path}?return_content=true"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["result"]

    def create_page_md(
        self,
        title,
        markdown_text,
        author_name=None,
        author_url=None,
        return_content=False,
    ):
        """
        Creates a new Telegraph page from markdown text.

        Args:
            title (str): Page title (1-256 characters).
            markdown_text (str): Markdown text to convert to HTML.
            author_name (str, optional): Author name (0-128 characters). Defaults to account's author_name.
            author_url (str, optional): Profile link (0-512 characters). Defaults to account's author_url.
            return_content (bool, optional): If True, return the content field in the response.

        Returns:
            str: URL of the created page.

        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        content = md_to_dom(markdown_text)
        return self.create_page(title, content, author_name, author_url, return_content)


ph = TelegraphAPI(access_token)


def md_to_dom(markdown_text):
    """Converts markdown text to a Python dictionary representing the DOM,
    limiting heading levels to h3 and h4.

    Args:
        markdown_text: The markdown text to convert.

    Returns:
        A Python list representing the DOM, where each element is a dictionary
        with the following keys:
            - 'tag': The tag name of the element.
            - 'attributes': A dictionary of attributes for the element (optional).
            - 'children': A list of child elements (optional).
    """

    # Convert markdown to HTML
    html = markdown.markdown(
        markdown_text,
        extensions=["markdown.extensions.extra", "markdown.extensions.sane_lists"],
    )

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    def parse_element(element):
        tag_dict = {"tag": element.name}
        if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            if element.name == "h1":
                tag_dict["tag"] = "h3"
            elif element.name == "h2":
                tag_dict["tag"] = "h4"
            else:
                tag_dict["tag"] = "p"
                tag_dict["children"] = [{"tag": "strong", "children": element.contents}]

            # Correctly handle children for h1-h6
            if element.attrs:
                tag_dict["attributes"] = element.attrs
            if element.contents:
                children = []
                for child in element.contents:
                    if isinstance(child, str):
                        # Remove leading/trailing whitespace from text nodes
                        children.append(child.strip())
                    else:  # it's another tag
                        children.append(parse_element(child))
                tag_dict["children"] = children
        else:
            if element.attrs:
                tag_dict["attributes"] = element.attrs
            if element.contents:
                children = []
                for child in element.contents:
                    if isinstance(child, str):
                        # Remove leading/trailing whitespace from text nodes
                        children.append(child.strip())
                    else:  # it's another tag
                        children.append(parse_element(child))
                if children:
                    tag_dict["children"] = children
        return tag_dict

    new_dom = []
    for element in soup.contents:
        if isinstance(element, str) and not element.strip():
            # Skip empty text nodes
            continue
        elif isinstance(element, str):
            # Treat remaining text nodes as separate elements for clarity
            new_dom.append({"tag": "text", "content": element.strip()})
        else:
            new_dom.append(parse_element(element))

    return new_dom


path = "Sample-Page-12-15"
print(json.dumps(ph.get_page(path), indent=4))

# Example usage:

# markdown_text = """
# # 大标题
# ## 小标题
# ### Heading 3
# #### Heading 4
# ##### Heading 5
# ###### Heading 6
# A paragraph of text.
# """
# content = md_to_dom(markdown_text)
# response = ph.edit_page("测试文章-06-19", "测试文章-06-19", content)
# print(response)
# path = "测试文章-06-19"
# print(json.dumps(get_page(path), indent=4))
