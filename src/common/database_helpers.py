from pony.orm.core import Entity
from copy import deepcopy

def _recursive_to_dict(dataset, **kwargs):
    print(type(dataset))
    assert isinstance(dataset, Entity)
    dataset = dataset.to_dict(**kwargs)
    print(dataset)
    for k, v in dataset.items():
        if isinstance(v, Entity):
            print("is instance in loop")
            print(v)
            v = v.to_dict(**kwargs)
            recursive_to_dict(v, **kwargs)
        dataset[k] = v.to_dict()
        print("to dict in loop")
        print(dataset)

    return dataset

def a_recursive_to_dict(dataset, iterated=None, **kwargs):
    if not iterated:
        iterated = []
    if isinstance(dataset, Entity):
        iterated.append(type(dataset))
        dataset = dataset.to_dict(**kwargs)
    for k, v in dataset.items():
        breaknow=False
        if isinstance(v, Entity):
            print(iterated)
            for instance in iterated:
                if isinstance(v, instance):
                    print("deleting {0}".format(k))
                    del dataset[k]
                    breaknow = True
                    break
            if breaknow:
                break
            dataset[k] = recursive_to_dict(v, iterated,  **kwargs)

        try:
            no_related_objs_kwargs = deepcopy(kwargs)
            if no_related_objs_kwargs.get('related_objects'):
                no_related_objs_kwargs.pop('related_objects')
            new_l = []
            for i in v:
                if isinstance(i, Entity):
                    new_l.append(recursive_to_dict(i, iterated,
                                                   **no_related_objs_kwargs))
            dataset[k] = new_l
        except:
            pass

        # if hasattr(v, '__iter__') and not isinstance(v, Entity):
        #     no_related_objs_kwargs = deepcopy(kwargs)
        #     if no_related_objs_kwargs.get('related_objects'):
        #         no_related_objs_kwargs.pop('related_objects')
        #     v_iterable = [recursive_to_dict(i, **no_related_objs_kwargs) if
        #                   isinstance(i, Entity) else i for i in v]
        #     dataset[k] = v_iterable
            # for i in v:
            #     print("In for loop")
            #     if isinstance(i, Entity):
            #         no_related_objs_kwargs = deepcopy(kwargs)
            #         no_related_objs_kwargs.pop('related_objects')
            #         print(i.to_dict(**no_related_objs_kwargs))
    return dataset

def _check_pony_iterations(entity, already_iterated):
    if entity.__class__ in already_iterated:
        return False
    return True

def best_recursive_to_dict(dataset, _has_iterated=None, **kwargs):
    if not _has_iterated:
        _has_iterated = []

    if isinstance(dataset, Entity):
        _has_iterated.append(dataset.__class__)
        dataset = dataset.to_dict(**kwargs)

    for key, value in dataset.items():
        dicted = False
        if isinstance(value, (list, tuple)):
            try:
                # Check if its an iterable and to_dict it
                iterable_l = []
                for iterable in value:
                    if isinstance(iterable, Entity) and _check_pony_iterations(
                            iterable, _has_iterated):
                        iterable_l.append(iterable.get_pk())
                dataset[key] = iterable_l
                dicted = True
            except:
                # this means it wasn't an iterable
                pass

        if not dicted:
            if isinstance(value, Entity):
               dataset[key] = recursive_to_dict(value, _has_iterated, **kwargs)

    return dataset


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

