import setuptools
from subprocess import check_call
import os.path as osp
from pathlib import Path

install_requires = \
    [
        'pycocotools ;platform_system!="Windows"',
        'pycocotools-windows ;platform_system=="Windows"',
        'chardet',
        'imantics',
        'pandas',
        'openpyxl',
        'ddt @ git+https://github.com/zmfkzj/draw_detection',
        'pyside6 ;platform_system!="darwin"',
        'tensorflow>=2.5.0 ;platform_system!="darwin"'
    ]

root = Path(__file__).parent
check_call("conda install -y --file".split()+[str(root/"requirements.txt")])
setuptools.setup(
    name="dtsummary",
    version="1.0.2",
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