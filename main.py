import sys
import csv
import json
import pandas as pd
from operator import itemgetter

SOURCE_FILE = sys.argv[1]


def main():
    books_list = _read_source_file_to_list_of_dicts(SOURCE_FILE)
    user_input = _get_task_from_user_input()
    if user_input == "Q" or user_input == "q":
        print("Exiting program!")
        sys.exit(0)
    if user_input == "1":
        _print_all_books(books_list)
    if user_input == "2":
        _query_book(books_list)
    if user_input == "3":
        _add_new_book(books_list)

    _book_data_to_csv_file(books_list)

    print("Thank you for using this service! Exiting now.")


def _read_source_file_to_list_of_dicts(source_file):
    """
        Source file is a required argument.
     """
    books_list = []
    dataframe = pd.read_csv(source_file, dtype=str, sep=";")
    for _, book_row in dataframe.iterrows():
        book_row = book_row.to_dict()
        books_list.append(book_row)
    books_list = _sort_books(books_list)

    return books_list


def _sort_books(books_list):
    return sorted(books_list, key=itemgetter("YEAR", "BOOKNAME"))


def _get_task_from_user_input():
    print("Welcome to library!")
    print('\n', "Please define wanted course of action.")
    print('\n', "Press 1 and enter if you wish query all books from the library.")
    print('\n', "Press 2 and enter if you wish query one specific book from the library.")
    print('\n', "Press 3 and enter if you wish add new a book to the liberary.")
    print('\n', "Press letter Q and enter if you wish to exist from program.")
    user_input = input("Please give number or exit with Q:")

    return user_input


def _print_all_books(books_list):
    for books in books_list:
        print(json.dumps(books, indent=4, sort_keys=True))


def _query_book(books_list):
    """
        Query parameters can be empty but at least one query parameter has to exist.
    """
    print('\n', "Query a book from the library!")
    user_input =  _ask_user_input_for_a_book()
    if user_input:
        wanted_book = [book for book in books_list if all(query_item in book.items() for query_item in user_input.items())]
        if wanted_book:
            print('\n', "Found following results:")
            print(json.dumps(wanted_book[0], indent=4, sort_keys=True))
        else:
            print('\n', "No books found!")
    else:
        print('\n', "No query parameters! Exiting program.")
        sys.exit(0)


def _add_new_book(books_list):
    print('\n', "Add a new book to the library!")
    user_input =  _ask_user_input_for_a_book()
    if len(user_input) < 4:
        print('\n', "Not enough data about the book! Exiting program.")
        sys.exit(0)
    books_list.append(user_input)
    books_list = _sort_books(books_list)


def _book_data_to_csv_file(books_list):
    dataframe = pd.DataFrame(books_list)
    dataframe.to_csv("books.csv", sep=';', index=False)


def _ask_user_input_for_a_book():
    user_input = {}
    user_input["BOOKNAME"] = input("Please give name of the book:")
    user_input["AUTHORNAME"] = input("Please give author of the book:")
    user_input["YEAR"] = input("Please give year when the book was written:")
    user_input["ISBN"] = input("Please give ISBN of the book:")
    user_input = {k:v for k, v in user_input.items() if v}

    return user_input


if __name__ == "__main__":
    main()