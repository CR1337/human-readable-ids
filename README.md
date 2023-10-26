# human-readable-ids
A tool for generating non-human-readable ids to human-readable ids.

## Usage

To use this tool first instantiate a `HumanReadableIdManager` object.
```python
from human_readable_ids import HumanReadableIdManager

manager = HumanReadableIdManager()
```

You can also specify a `seed` in order to change the generated ids in a deterministic way.
```python
# manager = HumanReadableIdManager(seed=1234)
```

Then you can use the `generate_human_readable_id` method to generate a human-readable id from an arbitrary id. The method supports ids of type `bytes` and all types that implement `__str__`. However it was only tested for `str` and `int`.
```python
original_id = "test_id"
human_readable_id = manager.generate_human_readable_id(original_id)

print(human_readable_id)
```

```bash
pushchair-font-4
```

The `HumanReadableIdManager` object stores the generated id. You can convert from the human readable id to the original id and back using the `get_original_id` and `get_human_readable_id` methods respectively.
```python
print(manager.get_original_id(human_readable_id))
print(manager.get_human_readable_id(original_id))
```

```bash
test_id
pushchair-font-4
```

To check whether a `HumanReadableIdManager` object has as specific id you can use the `has_human_readable_id` and `has_original_id` methods.
```python
print(manager.has_human_readable_id(human_readable_id))
print(manager.has_original_id(original_id))

print(manager.has_human_readable_id("non-existent-id"))
print(manager.has_original_id("non-existent-id"))
```

```bash
True
True
False
False
```

Furthermore you can specify a default value for `get_original_id` and `get_human_readable_id` in case the id does not exist.
```python
print(manager.get_original_id("non-existent-id", default="default-id"))
print(manager.get_human_readable_id("non-existent-id", default="default-id"))
```

```bash
default-id
default-id
```

`HumanReadableIdManager` also implements `__len__` which returns the amount of human readable ids that have been generated yet.
```python
print(len(manager))
```

```bash
1
```

When you try to generate a human readable id from an id that has already been generated, the same human readable id will be returned.
```python
print(manager.generate_human_readable_id(original_id))
print(manager.generate_human_readable_id(original_id))
```

```bash
pushchair-font-4
pushchair-font-4
```

The creation of human readable ids is based in MD5 hashing. In the rare case that to different ids result in a hash collision, the `HumanReadableIdManager` will detect this and make sure that the human readable ids are different. It is therefore guaranteed that the `HumanReadableIdManager` will never return the same human readable id for two different ids.
