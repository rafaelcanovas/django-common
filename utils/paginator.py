from django.core import paginator


class Paginator(paginator.Paginator):
    """
    A special paginator that automatically prevents any errors when
    calling the `page` method. It also modifies the resulting `Page`
    object to contain only some specific pages in its page range, so
    the pagination itself remains clean, showing just a few pages even
    when there are lots and lots of them.
    """

    def __init__(self, object_list, per_page, **kwargs):
        if not 'allow_empty_first_page' in kwargs:
            kwargs['allow_empty_first_page'] = True

        super().__init__(object_list, per_page, **kwargs)

    def page(self, number, per_side=4):
        """
        Number must be either an int or a string. We handle any possible
        errors when calling `super().page()` by resetting the page
        number to either 1 or self.num_pages. Read more about the
        optional `per_side` argument in `_modify_page`.
        """

        if isinstance(number, str):
            number = int(number) if number.isdigit() else 1
        elif not isinstance(number, int):
            raise TypeError('Invalid type for "number": %s' % type(number))

        if number <= 0:
            number = 1
        elif number > self.num_pages:
            number = self.num_pages

        page = super().page(number)

        return self._modify_page(page, number, per_side)

    def _modify_page(self, page, number, per_side=4):
        """
        Here we modify the `Page` object to show only a few pages.
        Assuming this paginator has 15 pages, the number of pages shown
        will be always 9 (i.e., `per_side` * 2 + 1 with `per_side` = 4).

        The resulting `Page` object has some more attributes like
        `left_side`, `right_side`, and `page_range`. Differently from
        `Paginator.page_range`, this page's `page_range` will only show
        `per_side` * 2 + 1 numbers. Assuming the current page is 9,
        `left_side` will be [5, 6, 7, 8] and `right_side` will be
        [10, 11, 12, 13]; `page_range` will be
        `left_side` + [9] + `right_side`.

        If any of the sides is less than `per_side`, the other side will
        try to compensate it; assuming the current page is 4,
        `left_side` will be [1, 2, 3] and `right_side` will be
        [5, 6, 7, 8, 9]. `page_range` will still be
        [1, 2, 3, 4, 5, 6, 7, 8, 9] nonetheless.
        """

        rng = list(self.page_range)
        index = rng.index(number)

        left_side = rng[:index]
        right_side = rng[index+1:]

        len_left = len(left_side)
        len_right = len(right_side)

        if len_left == len_right == per_side:
            page.left_side = left_side
            page.right_side = right_side

        elif len_left >= per_side and len_right >= per_side:
            page.left_side = left_side[-per_side:]
            page.right_side = right_side[:per_side]

        elif len_left < per_side:
            offset = per_side * 2 - len_left
            page.left_side = left_side
            page.right_side = right_side[:offset]

        elif len_right < per_side:
            offset = per_side * 2 - len_right
            page.left_side = left_side[-offset:]
            page.right_side = right_side

        page.page_range = page.left_side + [number] + page.right_side

        return page
