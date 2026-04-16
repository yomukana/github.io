from os import listdir
import os
from pathlib import Path
from pydantic import BaseModel
from jinja2 import Template

class MyAssetData(BaseModel):
    href: str
    view_name: str

# Replace these with your own links or set to an empty list
MY_ASSETS: list[MyAssetData] = [
    MyAssetData(href="YOUR_MASTER_LINK", view_name="Master"),
    MyAssetData(href="YOUR_DOCTOR_LINK", view_name="Doctor"),
]

def read_assets() -> list[MyAssetData]:
    # This searches the assets folder for pdfs
    assets_path = Path(__file__).parent / "assets"
    if not assets_path.exists():
        return []
    
    pdfs = [os.path.splitext(f)[0] for f in listdir(assets_path) if os.path.splitext(f)[1] == ".pdf"]
    # Replace '[your-username]' with your actual GitHub username
    return [MyAssetData(href=f"https://[yomukana].github.io/assets/{filename}.pdf", view_name=filename) for filename in pdfs]

def create_page() -> None:
    # Set your website title here
    contents = {"page_title": "My Repository", "my_assets": MY_ASSETS + read_assets()}
    with (Path(__file__).parent / "template.html").open("r", encoding="utf-8") as f:
        template = Template(f.read())
    with (Path(__file__).parent / "index.html").open("w", encoding="utf-8") as f:
        f.write(template.render(contents))

if __name__ == "__main__":
    create_page()
