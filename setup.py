import setuptools

install_requires = \
    [
        'pycocotools',
        'chardet',
        'imantics',
        'pandas',
        'openpyxl',
        'opencv-python',
        'ddt @ git+https://github.com/zmfkzj/draw_detection',
        'pyside6 ;platform_system!="darwin"',
        'tensorflow>=2.5.0 ;platform_system!="darwin"'
    ]

setuptools.setup(
    name="dtsummary",
    version="1.1.5",
    author="zmfkzj",
    author_email="qlwlal@naver.com",
    description="디텍션 결과를 정리하기 위한 모듈",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'dts=dtsummary.main:main'
        ]
    }
)
