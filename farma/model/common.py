import sys
import argparse
import omegaconf
from datetime import datetime
from farma.model.config import Config


# -------------------------------------------------------------------------
# read_config
# -------------------------------------------------------------------------
def read_config(filename: str, config_class=Config):
    """
    Read configuration filename and initiate objects
    """
    # Configuration file initialization
    schema = omegaconf.OmegaConf.structured(config_class)
    conf = omegaconf.OmegaConf.load(filename)
    try:
        conf = omegaconf.OmegaConf.merge(schema, conf)
    except BaseException as err:
        sys.exit(f"ERROR: {err}")
    return conf


# -------------------------------------------------------------------------
# validate_date
# -------------------------------------------------------------------------
def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "not a valid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)
