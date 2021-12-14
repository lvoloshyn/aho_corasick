### Aho-Corasick

Based on https://github.com/abusix/ahocorapy

Allows searching not only strings, but any type of sequence.

```
from tokentree import TokenTree

tree = TokenTree()
tree.add([1, 2])
tree.add([3, 4])
tree.add([3, 4, 5])
tree.finalize()

print(tree.search([1, 3, 4, 5, 2]))  # [([3, 4], 1), ([3, 4, 5], 1)]
print(tree.search_one([1, 3, 4, 5, 2]))  # ([3, 4], 1)

print(tree.search([1, 3, 4, 5, 2], return_indices=True))  # [(2, 1), (3, 1)]
print(tree.search_one([1, 3, 4, 5, 2], return_index=True))  # (2, 1)
```

```
from tokentree import TokenTree

tree = TokenTree()
tree.add(["Hello", "."])
tree.add(["try", "some", "token"])
tree.add(["token", "phrases"])
tree.finalize()

print(tree.search(["Hello", "!", "Let's", "try", "some", "token", "phrases"]))
# [(['try', 'some', 'token'], 3), (['token', 'phrases'], 5)]

print(tree.search(["Hello", "!", "Let's", "try", "some", "token", "phrases"], return_indices=True))
# [(2, 3), (3, 5)]
```

```
from tokentree import TokenTree

tree = TokenTree()
tree.add("malaga")
tree.add("lacrosse")
tree.add("mallorca")
tree.add("mallorca bella")
tree.add("orca")
tree.finalize()

print(tree.search("My favorite islands are malaga and sylt."))  # [('malaga', 24)]
print(tree.search("My favorite islands are malaga and sylt.", return_indices=True)) # [(1, 24)]

```