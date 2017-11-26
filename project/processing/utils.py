def remove_ref(wikitext):
    return wikitext


def get_templates(tree, name):
    return [t for t in tree.filter_templates() if t.name.matches(name)]