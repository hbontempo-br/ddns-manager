import os


def get_environment_variable(
        variable_name,
        default_value=None):
    """
    Gets an environment variable value, assuming the default value if it is not
    already defined on the underlying operating system.

    :param variable_name: Environment variable name.
    :param default_value: Environment variable default value.
    :return: Environment variable value or default value.
    """
    variable_value = os.environ.get(variable_name, default_value)
    if not variable_value:
        raise AttributeError(f'Can\'t find a value for environment variable \'{variable_name}\'!');
    return variable_value
