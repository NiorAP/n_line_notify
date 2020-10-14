from setuptools import setup

setup(
    name='n_line_notify',
    packages=['line_notify'],
    url='https://github.com/NiorAP/ap_line_notify',
    license='MIT',
    author='Nior.A.P',
    author_email='nior.a.p@hotmail.com',
    description='Line Notify Library by Nior.A.P',
    keywords=['Python', 'Line API', 'Line Notify', 'Nior.A.P'],
    install_requires=['requests', 'numpy', 'imageio', 'validators'],
    include_package_data=True
)
