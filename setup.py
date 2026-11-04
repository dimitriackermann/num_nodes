from setuptools import setup

package_name = 'num_nodes'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    extras_require={'test': ['pytest']},
    zip_safe=True,
    maintainer='Dimitri Ackermann',
    maintainer_email='dimitri.ackermann@googlemail.com',
    description='Counter publisher/subscriber and add/subtract service server and client.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'counter_pub = num_nodes.counter_pub:main',
            'counter_sub = num_nodes.counter_sub:main',
            'calc_server = num_nodes.calc_server:main',
            'calc_client = num_nodes.calc_client:main',
        ],
    },
)
