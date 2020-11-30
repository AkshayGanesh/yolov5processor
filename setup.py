import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yolov5processor",
    version="1.0",
    author="Akshay G",
    author_email="akshayganes@gmail.com",
    description="Wrapper package for yolov5 inference:v3.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AkshayGanesh/yolov5processor/tree/v1.0",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires =[
        "Cython",
        "matplotlib",
        "numpy",
        "pillow",
        "PyYAML",
        "scipy>=1.4.1",
        "tensorboard",
        "tqdm",
        "torch==1.6.0",
        "torchvision==0.7.0"
    ]
)
