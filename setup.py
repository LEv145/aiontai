from distutils.core import setup
setup(
  name = 'aiontai',
  packages = ['aiontai'],
  version = '0.1',
  license='GPL',
  description = 'Async wrapper for nhentai API',
  author = 'Alekseyzz',                   
  author_email = 'thehentwill@gmail.com',
  url = 'https://github.com/alekseyzz/aiontai',
  download_url = 'https://github.com/AlekseyZz/aiontai/archive/refs/tags/0.1.tar.gz',
  keywords = ['HENTAI', 'ASYNC', 'NHENTAI', 'API'],
  install_requires=[
          'schema',
          'aiohttp',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)