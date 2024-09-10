
from diffsync import DiffSync
from diffsync.enum import DiffSyncFlags

from nautobot_ssot.jobs.base import DataSource

from nautobot_ip_acls.ssot.adapters import ExampleRemoteAdapter, ExampleNautobotAdapter

name = "An SSoT Example"

#####
# Defining the DataSource Job
#####
class ExampleYAMLDataSource(DataSource):
    """SSoT Job class."""

    def __init__(self):
        """Initialize ExampleYAMLDataSource."""
        super().__init__()
        self.diffsync_flags = self.diffsync_flags | DiffSyncFlags.SKIP_UNMATCHED_DST

    class Meta:
        name = "Example YAML Data Source"
        description = "SSoT job example to get data from YAML"
        data_target = "Nautobot (remote)"

    def run(
        self, dryrun, memory_profiling, *args, **kwargs
    ):  # pylint:disable=arguments-differ
        """Run sync."""
        self.dryrun = dryrun
        self.memory_profiling = memory_profiling
        super().run(dryrun, memory_profiling, *args, **kwargs)

    def load_source_adapter(self):
        self.source_adapter = ExampleRemoteAdapter()
        self.source_adapter.load()

    def load_target_adapter(self):
        self.target_adapter = ExampleNautobotAdapter(job=self, sync=self.sync)
        self.target_adapter.load()
