from hansken_extraction_plugin.runtime.extraction_plugin_runner import run_with_hanskenpy

from registry_filetime_plugin import RegistryFiletimePlugin


def main():
    run_with_hanskenpy(RegistryFiletimePlugin)


if __name__ == '__main__':
    main()
