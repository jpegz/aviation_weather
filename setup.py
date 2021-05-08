from setuptools import setup

setup(name='aviation_weather',
      version='0.2',
      description='Utility for getting aviation weather information',
      url='http://github.com/jpegz/jpegz_aviation_weather',
      author='José Peguero',
      author_email='jose@pegosaur.us',
      license='MIT',
      packages=['aviation_weather'],
      install_requires=['lxml', 'requests', 'xmltodict'],
      zip_safe=True)
