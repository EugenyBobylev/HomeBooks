import os
import re

from flask import redirect, render_template, request, url_for

from app import app
import app.bookspdf as pdf
import app.iniconfig as cfg

ROWS_PER_PAGE = 12

all_books = []
if not all_books:
    catalogs = cfg.read_paths()
    all_books = pdf.init(catalogs)


@app.route('/')
@app.route('/index')
@app.route('/page/<int:page>')
@app.route('/index/page/<int:page>')
def index(page=1):
    page = request.args.get('page', page, type=int)
    page_books: pdf.Pagination = pdf.paginate(all_books, page=page, per_page=ROWS_PER_PAGE)
    for book in page_books.items:
        book.set_cover()
    return render_template('index.html', books=page_books)


@app.route('/book')
def open_book():
    path = request.args.get('path')
    page = request.args.get('page')
    os.popen(f'okular "{path}"')
    return redirect(url_for('index', page=page))


@app.route('/settings')
def settings():
    _catalogs = cfg.read_paths()
    print(_catalogs)
    return render_template('settings.html', catalogs=_catalogs)


@app.route('/addcatalog')
def add_catalog():
    catalog = request.args.get('catalog')
    print(str(catalog))
    return redirect(url_for('settings'))


@app.route('/updatecatalogs')
def update_catalogs():
    return redirect(url_for('settings'))


def get_pdf_path(arg) -> str:
    pdf_path = ''
    match = re.search('path=(.*)', arg)
    if match:
        pdf_path = match.group(1)
    return pdf_path


# @app.route('/rename/<name>')
@app.route('/rename', methods=['POST'])
def rename_book(name=''):
    data = request.get_json()
    book_path = data["book_path"]
    book_name = data["book_name"]
    book_name += '.pdf'
    book_path = get_pdf_path(book_path)
    if book_path:
        book = pdf.create_book(book_path)
        idx = all_books.index(book)
        result = pdf.rename_book(book_path, book_name)
        ok = result[0]
        if ok:
            renamed_book_path = result[1]
            renamed_book = pdf.create_book(renamed_book_path)
            all_books[idx] = renamed_book
    return '', 204


@app.route('/tagschanged', methods=['POST'])
def tags_changed():
    data = request.get_json()
    book_path = data["book_path"]
    book_tags = data["book_tags"]
    book_path = get_pdf_path(book_path)
    if book_path:
        book = [book for book in all_books if book.pdf_name == book_path][0]
        book.set_tags(book_tags)
    return '', 204
