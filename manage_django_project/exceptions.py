class SettingsNotFound(FileNotFoundError):
    pass


class ModuleNotFound(ModuleNotFoundError):
    pass


class ConfigKeyError(KeyError):
    pass
