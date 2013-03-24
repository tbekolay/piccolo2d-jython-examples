from jip.dist import setup
from setuptools import find_packages

requires_java = {
    'dependencies': [
        # (groupId, artifactId, version)
        ('org.piccolo2d', 'piccolo2d-core', '1.3.1'),
        ('org.piccolo2d', 'piccolo2d-extras', '1.3.1'),
    ],
}

setup(
      name="Piccolo2D.Java examples",
      version="0.1.0",
      author="Trevor Bekolay",
      author_email="tbekolay@gmail.com",
      description=("Examples of using the Piccolo2D.Java zoomable GUI "
                   "framework in Jython."),
      license="MIT",
      keywords="Jython Piccolo",
      packages=find_packages(),
      requires_java=requires_java,
)
