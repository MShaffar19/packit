from .base import BaseConfig

from .version import version_config
from .license import license_config
from .packages import packages_config


class WrapFacilities(object):

    def __init__(self, config_section_name):
        self._default = set()
        self._registry = {}
        self._config_section_name = config_section_name

    def add_facility(self, name, target, default=False):
        self._registry[name] = target
        if default:
            self._default.add(name)

    def get_enabled_facilities(self, config):
        facilities_section = config.get(self._config_section_name, {})

        enabled_facilities = set()
        for facility_name in self._registry:
            is_enabled = None

            # if facility explicitly disabled in facilities config then we force it off
            if facilities_section:
                is_enabled = self._is_facility_enabled(facilities_section, facility_name)

            if is_enabled is None:  # facility config not provided
                # check whether facility config section present or facility is enabled by default
                is_enabled = facility_name in config or facility_name in self._default

            if is_enabled:
                enabled_facilities.add(facility_name)

        # TODO: check for unrecognized sections and/or facilities

        return {k: v for k, v in self._registry.items() if k in enabled_facilities}

    @staticmethod
    def _is_facility_enabled(option_dict, option_name, true_values=('1', 'yes', 'y', 'true', 't')):
        """
        :return: True if explicitly enabled, False if explicitly disabled, None if no value provided
        """
        if option_name not in option_dict:
            return

        return option_dict[option_name].lower() in true_values

wrap_facilities = WrapFacilities('facilities')


wrap_facilities.add_facility('auto-version', version_config, default=True)
wrap_facilities.add_facility('auto-license', license_config, default=True)
wrap_facilities.add_facility('packages-config', packages_config, default=True)