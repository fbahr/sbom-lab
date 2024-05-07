Install SBOM generators using the following links and make sure to save them
using the mentioned filenames (to match the names used in `eval-sboms.sh`):

Required:
- jbom (https://github.com/eclipse/jbom/releases/) should be saved as `jbom.jar`.
- Syft (https://github.com/anchore/syft/releases/) should be saved as `syft`.
- Sbomgen (https://docs.aws.amazon.com/inspector/latest/user/sbom-generator.html)
  should be made available as `sbomgen`.

Optional:
- Trivy (https://github.com/aquasecurity/trivy/releases) should be saved as `trivy`.

The CycloneDX Maven Plugin will be downloaded by Maven and does not need to be
installed.
