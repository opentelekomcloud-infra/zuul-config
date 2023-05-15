# zuul-config

Repository with the Zuul configuration.

- `containers` - docker images to be used for pods based testing

- `nodepool` - nodepool configuration

- `tools` - diverse tools (i.e. for rendering zuul config from file based
  elements)

- `zuul` - tenant config (configuration elements to be combined by
  `tools/render_config.py`)

- `zuul.d` - Zuul configuration of the project itself (lint jobs, building
  container images, etc) 
