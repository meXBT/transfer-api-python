from setuptools import setup

setup(name='mexbt_transfer_api',
      version='0.3',
      description='A lightweight python client for the meXBT Transfer API',
      url='http://github.com/meXBT/transfer-api-python',
      author='meXBT',
      author_email='william@mexbt.com',
      license='MIT',
      packages=['mexbt_transfer_api'],
      install_requires=['requests'],
      zip_safe=False)
