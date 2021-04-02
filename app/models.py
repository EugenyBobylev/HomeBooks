from pathlib import Path

from app.mupdf import get_cover_fn, get_cover_png_fn, cover_exists, save_cover
from app.xattrpdf import get_meta_tags, set_meta_tags


class Book(object):
    pdf_name: str = ''
    book_name: str = ''
    cover = None
    tags = ''

    def __init__(self, path):
        self.pdf_name = path
        self.book_name = Path(path).stem
        self.get_tags()
        self.set_cover()

    def get_tags(self):
        self.tags = get_meta_tags(self.pdf_name)

    def set_tags(self, tags: str):
        set_meta_tags(self.pdf_name, tags)
        self.tags = tags

    def set_cover(self):
        """
        set file name to cover image and if cover image do not exists then create the cover image
        """
        self.cover = get_cover_fn(self.pdf_name)  # file name of cover image without path
        cover_png_fn = get_cover_png_fn(self.cover)  # path and file name of cove image
        exists = cover_exists(cover_png_fn)
        if not exists:
            save_cover(self.pdf_name, cover_png_fn)

    def exists(self) -> bool:
        return Path(self.pdf_name).exists()

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return self.pdf_name == other.pdf_name

    def __repr__(self):
        return f'cover: {self.cover}'


class Catalog(object):
    catalog: str = ''

    def __repr__(self):
        return f'{self.catalog}'
