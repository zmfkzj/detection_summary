import setuptools
from subprocess import check_call

install_requires = \
    [
        'pycocotools ;platform_system!="Windows"',
        'pycocotools-windows ;platform_system=="Windows"',
        'chardet',
        'imantics',
        'pandas',
        'openpyxl',
        'ddt @ git+https://github.com/zmfkzj/draw_detection',
        'pyside6'
    ]

check_call("conda install -y --file requirements.txt".split())
setuptools.setup(
    name="dtsummary",
    version="1.0.0",
    author="zmfkzj",
    author_email="qlwlal@naver.com",
    description="디텍션 결과를 정리하기 위한 모듈",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'dts=dtsummary.main:main'
        ]
    }
)