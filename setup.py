from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(name='geofinder',
      description='Track your Android device',
      version='0.1',
      author='Arthur Brenaut',
      author_email='arthur.brenaut@gmail.com',
      packages=find_packages(),
      install_requires=reqs,
      zip_safe=False)
