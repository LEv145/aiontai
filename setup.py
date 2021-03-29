from setuptools import setup

readme = ""
with open("README.md", "r") as long_description:
  readme = long_description.read()


setup(
  name = "aiontai",
  packages = ["aiontai"],
  version = "1.1",
  license="GPLv2",
  description = "Async wrapper for nhentai API",
  long_description=readme,
  long_description_content_type="text/markdown",
  author = "Alekseyzz", 
  author_email = "thehentwill@gmail.com",
  url = "https://github.com/alekseyzz/aiontai",
  download_url = "https://github.com/AlekseyZz/aiontai/archive/refs/tags/1.1.tar.gz",
  project_urls = {
    "Bag tracker":  "https://github.com/AlekseyZz/aiontai/issues",
    "Contributing": "https://github.com/alekseyzz/aiontai#contributing",
    "Source": "https://github.com/alekseyzz/aiontai",
    "Documentation": "https://github.com/AleksepyZz/aiontai/blob/main/README.md"
  },
  keywords = ["HENTAI", "ASYNC", "NHENTAI", "API"],
  install_requires=[
          "schema",
          "aiohttp",
      ],
  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
    "Topic :: Internet",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
  ],
)