import setuptools

setuptools.setup(
    name="climatemap",
    version="0.1",
    author="Maile Sasaki",
    author_email="mailes2@illinois.edu",
    description="A script to access downscaled CMIP6 data for use in Illinois",
    long_description_content_type="text/markdown",
    url="https://github.com/mailesasaki/climate_map",
    scripts=['LOCA2/LOCA2_download.py',
             'LOCA2/LOCA2_processor.py',
             'NEX_GDDP_CMIP6/nex_gddp_cmip6_download_il.py',
             'NEX_GDDP_CMIP6/NEX_GDDP_CMIP6_processor.py',
             ],
    py_modules=['LOCA2.LOCA2_processor', 'NEX_GDDP_CMIP6.NEX_GDDP_CMIP6_processor'],
    packages=setuptools.find_packages(),
)
