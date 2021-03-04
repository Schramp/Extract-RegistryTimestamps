from hansken_extraction_plugin.api.author import Author
from hansken_extraction_plugin.api.extraction_plugin import ExtractionPlugin
from hansken_extraction_plugin.api.maturity_level import MaturityLevel
from hansken_extraction_plugin.api.plugin_info import PluginInfo
from logbook import Logger
from datetime import datetime
import struct
import pytz

# http://support.microsoft.com/kb/167296
# How To Convert a UNIX time_t to a Win32 FILETIME or SYSTEMTIME
EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970 as MS file time
HUNDREDS_OF_NANOSECONDS = 10000000

def filetime_to_dt(ft):
    """Converts a Microsoft filetime number to a Python datetime. The new
    datetime object is time zone-naive but is equivalent to tzinfo=utc.
    >>> filetime_to_dt(116444736000000000)
    datetime.datetime(1970, 1, 1, 0, 0)
    >>> filetime_to_dt(128930364000000000)
    datetime.datetime(2009, 7, 25, 23, 0)
    """
    try:
        unaware = datetime.utcfromtimestamp((ft - EPOCH_AS_FILETIME) / HUNDREDS_OF_NANOSECONDS)
        now_aware = unaware.replace(tzinfo=pytz.UTC)
        return now_aware
    except ValueError as e :
        return None

log = Logger(__name__)


class RegistryFiletimePlugin(ExtractionPlugin):

    def plugin_info(self):
        log.info('pluginInfo request')
        plugin_info = PluginInfo(
            self,
            name='python_registry_timestamps_plugin',
            version='0.0.1',
            description='Parse 8 byte FILETIME properties from binary registry',
            author=Author('R.Schramp', 'r.schramp@nfi.nl', 'NFI'),
            maturity=MaturityLevel.PROOF_OF_CONCEPT,
            webpage_url='https://hansken.org',
            matcher='type:registryEntry AND registryEntry.type=BIN AND $data.type=raw'
        )
        log.debug(f'returning plugin info: {plugin_info}')
        return plugin_info

    def process(self, trace, context):
        # log something to output as an example
        log.info(f"processing trace {trace.get('name')}")
        if  context.data_size() != 8:
            return
        with trace.open() as thedatahandle:
            thedata = thedatahandle.read(8)
            if len(thedata) == 8:
                filetime = struct.unpack("Q", thedata)[0]
                thedate = filetime_to_dt(filetime)
                if filetime > 0 and not thedate is None and thedate.year > 2010 and thedate.year < 2022:
                    trace.update("event.createdOn", thedate)
                    trace.update("event.application", "registrytimestamp")
                    keyname = trace.get("registryEntry.key")
                    log.debug(f"{keyname},{thedate},{filetime}")

