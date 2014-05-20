from django import template

register = template.Library()


@register.filter
def annotate_comment_tree(comments):
    """
    Iterate through nodes and add 'open' and 'close' attributes
    """
    if not comments:
        return

    it_comments = iter(comments)

    # get the first item, this will fail if no items !
    current = it_comments.next()

    # first item starts a new thread
    current.open = True
    current.close = []

    for next_c in it_comments:
        next_c.open = False
        # if the level of the next comment is higher then current
        # open a new thread
        if next_c.level > current.level:
            next_c.open = True
        # in any other case, calcualte how many comments we need to close
        else:
            current.close = range(current.level - next_c.level)

        # return current comment
        yield current
        current = next_c

    # return last comment
    current.close = range(current.level + 1)
    yield current
