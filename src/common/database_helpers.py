from pony.orm.core import Entity

def recursive_to_dict(dataset, _has_iterated=False, **kwargs):
    if isinstance(dataset, Entity):
        dataset = dataset.to_dict(**kwargs)

    delete_these = []
    for key, value in dataset.items():
        if _has_iterated:
            if isinstance(value, (list, tuple)):
                for iterable in value:
                    if isinstance(iterable, Entity):
                        delete_these.append(key)
                        break
                continue
        else:
            if isinstance(value, (list, tuple)):
                value_list = []
                for iterable in value:
                    if isinstance(iterable, Entity):
                        value_list.append(recursive_to_dict(iterable, True,
                                                            **kwargs))
                dataset[key] = value_list


        if isinstance(value, Entity) and not _has_iterated:
           dataset[key] = recursive_to_dict(value, True, **kwargs)

        elif isinstance(value, Entity) and _has_iterated:
            delete_these.append(key)

    for deletable_key in delete_these:
        del dataset[deletable_key]

    return dataset

def easy_dict(data, show_hidden=False, show_related=True):
    local_kwargs = {}
    if show_hidden:
        local_kwargs.update({'with_lazy': True, 'with_collections': True})
    if show_related:
        local_kwargs.update({'related_objects': True})
    return recursive_to_dict(data, **local_kwargs)


