import setuptools

install_requires = \
    [
        'pycocotools-windows',
        'chardet',
        'imantics',
        'openpyxl',
        'ddt @ git+https://github.com/zmfkzj/draw_detection',
    ]

setuptools.setup(
    name="dtsummary",
    version="0.0.1",
    author="zmfkzj",
    author_email="qlwlal@naver.com",
    description="디텍션 결과를 정리하기 위한 모듈",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires=">=3.8",
)