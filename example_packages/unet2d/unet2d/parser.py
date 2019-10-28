"""Provide a parser."""
from importlib import import_module

import torch.nn as nn
import torch.optim as optim

import unet2d.data as datasets
import unet2d.transforms as core_trafos


def get_class(name, packages):
    """Return a class in packages."""
    for pkg in packages:
        if hasattr(pkg, name):
            return getattr(pkg, name)
    raise AttributeError("Did not find %s" % name)


def parse_train_config(train_config, model):
    """Parse the training config."""
    loss_config = train_config["loss"]
    loss = get_class(loss_config["name"], [nn])(**loss_config.get("kwargs", {}))

    transform_config = loss_config.get("transformations", [])
    transforms = [
        get_class(trafo["name"], [core_trafos])(**trafo.get("kwargs", {}))
        for trafo in transform_config
    ]

    optimizer_config = train_config["optimizer"]
    optimizer = get_class(optimizer_config["name"], [optim])(
        model.parameters(), **optimizer_config.get("kwargs", {})
    )

    batch_size = train_config["batch_size"]

    pretrained_conf = train_config["pretrained_on"]
    # This needs to be more sophisticated in practice
    # need to support concatenating multiple datasets
    # need to support custom urls/dois and validate hashes
    ds_config = pretrained_conf["datasets"][0]
    ds = get_class(ds_config["name"], [datasets])()

    n_iterations = pretrained_conf["n_iterations"]

    return {
        "loss": loss,
        "optimizer": optimizer,
        "transforms": transforms,
        "batch_size": batch_size,
        "dataset": ds,
        "n_iterations": n_iterations,
    }


def parse_data_config(data_config):
    """Parse the data config."""
    in_config = data_config["input_transformations"]
    in_transforms = [
        get_class(trafo["name"], [core_trafos])(**trafo.get("kwargs", {}))
        for trafo in in_config
    ]

    out_config = data_config["output_transformations"]
    out_transforms = [
        get_class(trafo["name"], [core_trafos])(**trafo.get("kwargs", {}))
        for trafo in out_config
    ]

    return {"input_transforms": in_transforms, "output_transforms": out_transforms}


def parse_model_config(model_config):
    """Parse the model config."""
    definition = model_config["definition"]
    module_name = definition["name"]
    kwargs = definition.get("kwargs", {})
    module_names = module_name.split(".")
    model_module = import_module(".".join(module_names[:-1]))

    if not getattr(model_module, module_names[-1]):
        raise RuntimeError("Class name %s does not exist" % module_names[1])
    model = getattr(model_module, module_names[-1])(**kwargs)
    return model


def parse_config(config):
    """Parse the config."""
    model = parse_model_config(config["model"])
    train_dict = parse_train_config(config["training"], model)
    data_dict = parse_data_config(config["data"])
    return model, train_dict, data_dict
