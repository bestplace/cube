c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.token = ''

# Timeout (in seconds) after which a kernel is considered idle and ready to be culled.
c.MappingKernelManager.cull_idle_timeout = 3 * 24 * 3600
# The interval (in seconds) on which to check for idle kernels exceeding the cull timeout value.
c.MappingKernelManager.cull_interval = 300
